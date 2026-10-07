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

Base: Workspace `057b727cc7e6528bac212777addafc730dfa1a46`, tree
`9541ee678280032211b8c74811bbd1e65a95e9ba` (accepted #690 / PR #697 merge).
The locked product and source-profile identities remain distinct from this
extension delivery. CFRU, DPE, UPR-FVX, Tracker, NatDexExtension and all Gitlinks
are unchanged. The T1 generator and generated `source-data.json` are unchanged.
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

## Verification on the Mac host

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

## Next handoff

CONTROL reviews the candidate PR, including the explicit Lua `NOT_RUN` gap;
Phase A acceptance remains pending actual mock execution on an allowed runtime.
Do not close #691 or route live integration until Phase B's existing gates pass.
