# T2 Phase A — source/mock guard candidate

Contract: [Workspace #691](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/691),
under [#500](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/500).
CONTROL authorized Mac-only / ROM-free / synthetic work on 2026-10-07.

**CONFIRMED CURRENT STATE:** implementation and source checks are present.
**UNKNOWN / NOT_RUN:** Lua execution, including mock behavior, syntax and the
portable SHA-256 implementation. No installed Lua 5.1/5.4 executable, LuaJIT,
Python Lupa, Node Lua package or Vim Lua support was available on this Mac.
No runtime or package was installed. The Phase A exit marker
`CFRUDPE_EXTENSION_PROFILE_MOCK_GUARD_READY` is **NOT_ESTABLISHED** until the
mock suite actually passes. The production marker is not achieved, and #691
must remain open. This candidate requires review before acceptance.

## Revision and protected boundaries

Original branch base: Workspace `057b727cc7e6528bac212777addafc730dfa1a46`, tree
`9541ee678280032211b8c74811bbd1e65a95e9ba` (accepted #690 / PR #697 merge).
Accepted #699 / PR #700 main `f7cde29ece11fa648a88ea5c2f88cb394264cf1d`, tree
`e230c547e78c67f8a33a61d273f4d60a64fe3aea`, was integrated with a regular merge
on the same `feature/691-extension-mock-activation` branch. Both #699 identity
documentation and #691 Phase A limitations were retained without conflicts.
The locked product and source-profile identities remain distinct from this
extension delivery. CFRU, DPE, UPR-FVX, Tracker, NatDexExtension and all Gitlinks
are unchanged. The T1 generator and generated `source-data.json` exactly match
accepted main; this continuation changes neither file after integrating #699.
The known untracked `CASUAL_NATDEX.rnqs` was neither opened nor staged.
No game artifacts, builds, private paths, local manifests or `offsets.ini`
were used. No emulator, real Tracker runtime or memory session was run.

## Implementation boundary

- Public source validation hashes the **entire exact canonical T1 JSON bytes**
  against a pinned SHA-256 before decoding. The content lock covers all pins,
  schema, configuration, mapping, layout, provenance and unknown/extra keys;
  a self-declared or recomputed `profileId` cannot authorize a different profile.
  The profile's historical extension-compatibility declaration is preserved;
  v2 source parsing does not promote its runtime support from `UNRESOLVED`.
- `beforeGameDataLoad` replaces `GameSettings.initialize` with an owned stop
  guard. Production always sets `Unsupported Game`, disables the LR memory-write
  option, publishes `UNKNOWN` and does not call stock initialization or read
  memory/filesystem manifests. No profile selector or mocked identity can open
  the production path. Enabling after initialization requests a guarded restart.
- A separate factory creates a detached mock host only outside a Tracker/emulator
  environment. Its closed-over test mode cannot change the production instance.
  Successful synthetic validation is `TEST_ONLY`; live confidence stays
  `UNKNOWN`, and `gamename` stays `Unsupported Game` even in the success fixture.
- The in-memory binding is explicitly `SYNTHETIC_ONLY`. Only the player/enemy
  party lifecycle dependency set is modeled: exact profile/Tracker/extension,
  synthetic output/session/epoch, source-backed fixed descriptors, domain, read
  width, full party span/alignment and pre/post identity/session checks.
  Repoint anchors, unresolved chains, numeric strings and extra/missing bindings
  are rejected. No pointer probing or T3/T4 decoder is implemented.
- An extension-owned adapter applies only validated `GameSettings.pstats`,
  `estats`, party count, four `Program.Addresses` structure sizes and two
  `PokemonData.Addresses` source offsets. The complete expected manifest is
  required. Deterministic journaling and assertions at effective nested consumer
  paths reject false, partial, dropped or thrown imports and undo applied values.
  The pinned filesystem JSON importers are deliberately bypassed because their
  success flag and flat writes do not satisfy the contract. A mocked in-memory
  transport can inject partial failures into the same transaction.
- Invalidations clear binding, confidence, context, diagnostic values and
  snapshots, advance the epoch and revoke the accepted mock session epoch.
  Per-frame/update checks detect changed identity/session, overrides, wrappers
  or an enabled LR write option. Recovery requires fresh synthetic proof.
- Unload restores owned overrides and initializer references, preserves later
  owners' replacements and requests a restart. One **safety tombstone** remains
  on the persistent `IronmonTracker.startTracker` entry, preventing stock
  reinitialization after disable/reload, including reconstructed module tables.
  This intentional stop guard is not an active data adapter. A new host process
  is outside the tombstone's lifetime; real host/reset/output detection and
  conflicts with other persistent restart wrappers remain Phase B unknowns.
- The executable legacy diagnostic reader has been superseded by inert getters.
  Its immutable [baseline source](https://github.com/Planton361/firered-gen9-randomizer-workspace/blob/057b727cc7e6528bac212777addafc730dfa1a46/03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua)
  and historical layout/offset/runtime evidence remain available. No historical
  plausibility test becomes current acceptance.

Party decoding, live battle values, normal UI/derived-data adapters and
persisted Tracker consumer coverage remain `UNAVAILABLE` here and belong to
T3–T5. This candidate blocks initial production module loading; it does not
claim complete T5 UI coverage or integration API sufficiency.

## Initial verification before the first T2 commit

The following PASS results were obtained before committing the extension change,
while Git HEAD still contained the T1 extension blob. They are historical evidence;
the subsequent historical T1 lock failure and its resolution are recorded below.

| Check | Result |
| --- | --- |
| New public-lock, forbidden-input/write-call, pinned seam and nested-consumer source checks | **PASS — 4 tests** |
| Existing #690 source/parser/ABI/synthetic regression suite | **PASS — 24 tests** |
| T1 `--check`, exact regeneration | **PASS — byte-identical** |
| Python runner/source-test compilation | **PASS** |
| Lua mock suite, Lua syntax, SHA known-answer vectors | **NOT_RUN — no installed compatible runtime; runner exits 2** |
| Both Lua 5.1 / 5.4 execution compatibility | **NOT_RUN** |
| Git safety, explicit-file/Gitlink review, whitespace check | **PASS** |
| Linux/BizHawk, real Tracker load/unload/output binding, emulator memory | **NOT_RUN / PENDING_LINUX_HOST** |

Reproduce the available source checks:

```sh
python3 -m unittest discover -s 07_scripts/tracker -p 'test_cfru_dpe_extension_source.py' -v
python3 -m unittest discover -s 07_scripts/tracker -p 'test_generate_cfru_dpe_source_data.py' -v
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py --check
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check
```

Run the Lua suite only using an already available permitted runtime:

```sh
python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py
# Optional explicit existing executable:
python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua lua5.4
```

The runner supplies public source text plus in-memory synthetic objects via
stdin. It never creates/reads a local runtime manifest. Missing runtimes produce
`NOT_RUN`, not PASS. Cases cover source/schema/pin corruption, missing manifests
and dependencies, bad addresses/provenance, partial imports/read-back, failed
reads, conflicts, restart, late enable, repeated disable, unload and stale epochs.
Mock write functions raise `FORBIDDEN memory write`; ordinary cases assert zero
invocations, and one negative injection asserts the attempted call is rejected
as a lifecycle failure without any memory backend.

## CONTROL repair — accepted-session early reentry

The review of PR #698 at `6f0b9d0fac67c1b803dfebc0059a5da2ef741174` found that
`beforeGameDataLoad()` cleared published state without revoking the accepted
internal session. The repair explicitly records that session/epoch as revoked
and clears `accepted` / `source` before rollback and early-guard setup. Repeated
hooks before the first acceptance remain idempotent; owned wrappers are retained.

The added Lua regression accepts epoch 1, reenters the early hook, checks rollback,
snapshot invalidation and wrapper references, rejects epoch 1 before memory reads,
and rejects advancing the host epoch without a fresh binding. A fresh synthetic
epoch-2 binding must pass the complete transaction and session checks to recover
`TEST_ONLY`; live confidence remains `UNKNOWN`. This regression is **NOT_RUN**.

Historical rerun at `89d1df2b8c9ccf80a976781b47d658793af55af5`, before #699:

| Repair check | Historical result |
| --- | --- |
| Phase A source tests | **PASS — 4 tests** |
| T1 parser tests | **PASS — 8 tests** |
| Full Tracker Python discovery | **FAIL — 12 tests pass; 16 profile tests blocked by class setup** |
| T1 generator `--check` | **FAIL — `Unreviewed extension revision`** |
| Python compilation, Git safety, whitespace and explicit-file/Gitlink review | **PASS** |
| Lua suite including reentry regression, syntax, SHA vectors and 5.1/5.4 execution | **NOT_RUN — no installed compatible interpreter; runner exits 2** |
| Production activation / Linux-BizHawk acceptance | **UNKNOWN / NOT_RUN; activation remains denied** |

At that revision the unchanged T1 generator checked `HEAD:CFRUDPEExtension.lua` against its historical
`294cac84152e87010eb806c6331c90100d204a83` blob. The committed T2 extension differs,
so `LockedSources` rejects it before source regeneration/profile tests. This also
affects the previously reviewed T2 commit, not just the three-line reset repair.
The Phase A source checks still confirm the unchanged public JSON byte hash.
Generator, profile JSON and Gitlinks were unchanged by that repair. #699 resolved
this independent lock compatibility issue within its own source-contract branch;
the accepted result is integrated below. The old pre-commit PASS was not evidence
of that repair revision's T1 regression PASS.

No tools were installed. `CFRUDPE_EXTENSION_PROFILE_MOCK_GUARD_READY` remains
**NOT_ESTABLISHED** until actual permitted Lua execution passes and review defects
are cleared; PR #698 remains DRAFT and #691 remains OPEN.

## Accepted #699 identity integration and current verification

The extension now locks the accepted public profile from merged #699. Only its
`SOURCE_SHA256` and `PROFILE_ID` constants change; production denial and the
accepted-session reentry repair remain intact. The Lua mock runner derives its
in-memory source/profile fixtures directly from the accepted public JSON, and
binding fixtures derive `profileId` from that injected profile. No fixture keeps
an old hardcoded identity or creates a local runtime manifest.

| Accepted identity | Value |
| --- | --- |
| Canonical profileId | `sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75` |
| source-data.json SHA-256 | `8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981` |
| Generator SHA-256 | `9c6fcf0a631557defaef64f5ac78db8df483d359d4f6e7a4708011ee2dd70beb` |

| Current continuation check | Result |
| --- | --- |
| Full T1 source/parser/ABI/synthetic suite | **PASS — 29 tests** |
| Phase A source checks | **PASS — 4 tests**, including exact accepted public JSON hash/identity |
| T1 generator `--check` | **PASS — byte-identical** |
| Python compilation | **PASS** |
| Git safety, whitespace, explicit-file/Gitlink and merge ancestry review | **PASS** |
| Lua mock suite, accepted-session reentry, syntax and SHA known-answer vectors | **NOT_RUN — no permitted compatible runtime on PATH; runner exits 2** |
| Lua 5.1 and Lua 5.4 execution coverage | **NOT_RUN**, each interpreter unavailable |
| Linux/BizHawk, real Tracker output/session binding and read-only memory acceptance | **NOT_RUN / PENDING_LINUX_HOST** |

These source checks are rerun after the identity update commit; its exact revision
and results are recorded in Draft PR #698. The former T1 extension-HEAD lock
blocker is resolved. The independent Lua execution gate remains open. No tools
were installed, no Phase A completion is claimed, and production remains denied.

## Next handoff

CONTROL reviews the updated Draft PR #698, including the remaining Lua `NOT_RUN`;
Phase A acceptance remains pending actual mock execution on an allowed runtime.
Do not close #691 or route live integration until Phase B's existing gates pass.
