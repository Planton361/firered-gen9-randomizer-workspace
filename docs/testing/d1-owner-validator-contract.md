# D1 owner/write-set receipt validator — #727

**CONFIRMED USER DECISION:** Implementation authority is
[#727 comment 6382839930](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/727#issuecomment-6382839930).
Only the validator, its synthetic test file and this contract are changed.
Branch: `audit/727-d1-owner-validator`; parent Workspace revision:
`3cbb0c9ec86aa5c99d2d0370884df47481e7405e`.

**CONFIRMED CURRENT STATE:** This is an offline, fail-closed **receipt
consistency validator**, with no ROM reader, build runner, patch implementation
or native observer. It can reject a supplied inconsistent write-set before
any insertion. It cannot certify that a supplied receipt is true or complete.
Every invocation returns `D1_ALL=FAIL` or `D1_ALL=UNKNOWN`; there is deliberately
no success/override mode. It does not create an UPR ownership witness.

**UNKNOWN / STOP:** The independent original-inserter observation, actual
source/configuration and fresh-build identity, native link/ABI correctness,
actual selected output identity, and DPE reproducibility are unproved.
**CFRU insertion remains unauthorized.** Even a receipt passing all six
consistency checks does not unlock insertion, UPR Stage B, D2+, merges or pins.
No private artifact was used to implement or test this helper.

## Revision and live preflight evidence

At implementation, live Project #4 had #727 as the sole Doing item, P0,
Component Delivery. #726 and #741 were Ready; #741 P1. The approval and all
three Issues were read live. This records that observation, not a new queue.
Workspace started detached at the parent above. The approved branch was absent
locally and remotely before creation in this existing Workspace.

Selected public source IDs are fixed in code:

| Component | Public revision |
| --- | --- |
| CFRU | `196058edbc2b8b7d8c725b715b1f967ba60f5c83` |
| DPE | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| UPR | `e1127cfde58af359e458f8d6a19339f3db3c8589` |

Actual submodule checkouts matched these public IDs. Workspace Gitlinks still
pointed to CFRU `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2`, DPE
`d887185de1f6ae6a78e85c4311bbadde17041d00`, UPR
`4670a5413104ec02bc08c09ff584470a8a6cb7bd`. The two known CFRU/UPR checkout
differences are preserved and excluded from the commit. Tracked component
worktrees reported no changes. These facts do not establish private build
cleanliness or accept these candidates as integration pins.

## USER-ONLY invocation and safe result

USER alone supplies an existing independent receipt as private local JSON.
Set `D1_RECEIPT` locally to its filename, then run from the original Workspace:

```sh
python3 -B 07_scripts/d1/validate_owner_write_sets.py --receipt "$D1_RECEIPT"
```

Do not upload this JSON, private filenames, offsets, hashes, symbol/link maps,
source inventories, logs, binaries, ROMs, images, config bytes or tool data.
Do not construct a receipt by guessing free bytes or copying old manifests.
No receipt exists as a result of these public tests. With no independently
captured receipt, omit the argument to obtain fixed UNKNOWN statuses without
opening any file. The helper opens only the explicitly supplied JSON, up to
16 MiB. It never follows fields as filenames, executes tools, calls inserters,
writes files, or reads ROM/build/map/tool data referenced by a receipt.

Only the following fixed keys and `PASS|FAIL|UNKNOWN` values are printed:

| Gate | Meaning |
| --- | --- |
| `D1_RECEIPT_SCHEMA` | Exact version, public source IDs, root structure and digest syntax |
| `D1_RECEIPT_PROVENANCE` | Declared fresh builds, generated/cache inventories, payload binding and DPE-output → CFRU-input identity chain |
| `D1_WRITE_ORDER` | Explicit complete phase lists, phase/write counts, sequence, declared intermediate state chain and final output binding |
| `D1_CAPACITY` | Declared binary/allocation capacity, appended overlays, physical bounds and dynamic allocator reservations |
| `D1_DECLARED_OWNERS` | Disjoint declared physical leaves, required roles, size/alignment constraints and critical alias rejection |
| `D1_WRITE_SETS` | Claimed owner containment, hook/pointer targets, allocation use and explicit ordered overrides |
| `D1_ORIGINAL_OBSERVATION` | Always UNKNOWN: no independent complete original-path observer |
| `D1_SOURCE_CONFIG_IDENTITY` | Always UNKNOWN: actual source/config artifacts not independently inspected |
| `D1_FRESH_BUILD` | Always UNKNOWN: declared receipt freshness is not actual fresh-build proof |
| `D1_NATIVE_BUILD_LINK_INSERT` | Always UNKNOWN: actual link/insertion and ARM semantics not observed |
| `D1_OAK_ABI` | Always UNKNOWN: declared sizes do not prove emitted ABI or installed contents |
| `D1_OUTPUT_PROVENANCE` | Always UNKNOWN: no independent selected-output comparison |
| `D1_DPE_REPRODUCIBILITY` | Always UNKNOWN: #741 is not repaired or rerun here |
| `D1_ALL` | FAIL if any check fails; otherwise UNKNOWN |

Exit **1** means a contradiction/malformed receipt was found; exit **2** means
UNKNOWN/STOP. Exit 0 is never returned. Missing evidence stays UNKNOWN;
contradictory supplied evidence is FAIL. FAIL dominates the overall result.
Unavailable/unreadable input and invalid arguments yield UNKNOWN. Malformed,
duplicate-key, nonfinite-number, excessive-size or invalid-encoding JSON yields
FAIL. Exceptions never echo their text, arguments or tracebacks. Individual
consistency PASS results are scoped to the declared receipt only.

## Receipt version 1

All objects have exactly the keys listed below: missing keys are UNKNOWN,
extra keys or wrong types are FAIL. Arrays are limited to 10,000 entries each.
Integers exclude booleans. All intervals are nonempty half-open **file-offset**
intervals `[start,end)`, bounded by 32 MiB; ROM bus addresses are invalid.
IDs/roles/kinds are 1–80 ASCII alphanumeric/underscore/hyphen characters.
Digest fields are lowercase SHA-256 text. IDs are opaque local labels, never
printed. They are not symbols or proof of ownership.

The root contains `schema` (integer 1), `sources` (exact three public IDs above),
`config` (digest of the independently selected whole build configuration),
`builds`, `stages`, `allocations`, `owners`, `overrides`.

- A build contains `id`, `component` (`dpe` or `cfru`), `source`, `config`,
  `fresh` (true), `artifacts`. Exactly one build per component is required.
  Each artifact has `id`, `kind`, `build`, `sha256`, `cached` (false).
  Kinds must be unambiguous and include `linked`, `payload`, `generated`,
  `objects`, `repoint_cache`. Aggregate inventory digests must include every
  generated input/object/cache for the selected run. Even an empty regenerated
  repoint cache needs its current-run inventory entry. An inserter reusing
  an old generated cache must not be declared fresh.
- Stages occur exactly in DPE → CFRU order, with `component`, `build`, `input`,
  `output`, `input_size`, `output_size`, `completed` (true), `phases`, `writes`.
  Input/output are whole-image digests. CFRU input digest and size must match
  DPE output exactly. Both outputs and CFRU input must be 32 MiB. A failed or
  partial run is rejected, even if its last available snapshot looks valid.
- A phase has `name`, `status` (`done` or `absent`), `count` (actual ROM write
  count). Every phase appears exactly once in the order below. `absent`
  requires zero writes; copy, payload, offsets and DPE expand must be `done`.
  Copy initializes the stage input state; its file-copy operation is not
  double-counted as a ROM write. Offset-file output has zero ROM writes.
  Expansion has zero writes if input already has the final size.
- Each write has `id`, `seq` (zero-based within stage), `phase`, `kind`,
  `start`, `end`, `owner`, `allocation`, `before`, `after`, `input_state`,
  `output_state`, `target`, `scan`. Write IDs are globally unique. Range
  `before`/`after` digests and whole-image state digests must come from the
  real operation; the helper checks the chain, not the underlying bytes.
  An expanded previously absent range uses the digest of its actual empty
  preimage. Unchanged range and unchanged whole state must agree. Payload
  `after` must match the selected build's payload artifact digest.
- `kind` is `bulk` for payload, `expand` for expansion, `hook` for hooks,
  `wrapper` for function rewrites, `pointer` for repoint/routine/song paths,
  otherwise `data`. Events/overlays may additionally use `pointer` for
  existing event/map-header pointer writes. This preserves the distinction
  between appending an overlay and updating an existing map header.
- `owner` identifies a physical leaf containing the write; `allocation`
  must equal that leaf's allocation (or null). Bulk payload writes instead
  have null owner and name the exact entire payload allocation. Expansion
  has null owner/allocation and spans exactly input size to 32 MiB. Pointer,
  hook and wrapper writes carry `target` with `owner`, `offset` (physical,
  Thumb bit removed), `thumb` (boolean). Other writes have null target.
  Pointer writes are exactly 4 B. Hook writes use the original 8 B or 10 B
  width according to halfword/word alignment. Hooks, routine pointers and
  wrappers require an even target offset and true Thumb flag. Actual
  encoded target bytes, wrapper parameter-dependent machine code, r0/r1,
  stack/call-return behavior and relocations remain native UNKNOWN gates.
- `scan` is `source` for CFRU `repoint_all`, `current` for DPE `repoint_all`,
  otherwise `none`. Original dynamic scans, ignored offsets, slide factors,
  conditional configuration, all resolved matches and generated-cache
  suppression must be observed independently. A list of guessed matches
  does not establish scan completeness.

## Original write paths and order

The source baseline is the pinned public `scripts/insert.py` in each component,
read from Git objects rather than local generated/mutable build scripts.
The validator models these distinct sequences; it does not reimplement them:

```text
DPE:  copy → expand → payload → bytepatch → special → hooks → repoints
      → generated_repoints → repoint_all → routine_pointers
      → function_rewrites → offsets
CFRU: copy → payload → generated_repoints → repoint_all → special
      → free_bytepatch → bytepatch → hooks → repoints → routine_pointers
      → function_rewrites → events → overlays → songs → offsets
```

Includes byte replacements, special inserts, cached/direct/scanning repoints,
hooks, function wrappers, free-byte allocations, event/object/warp/coord/BG
script repoints, appended map-object/coord/event-header data and existing
header repoints, songs and generated offset/cache side effects as inventory
obligations. Within a phase the actual original operation order must be
retained, including per-byte writes, no-op writes and superseded writes.
A final byte diff alone cannot expose these paths. Cache and offset-file
side effects are provenance inventory obligations, not ROM intervals.

An independently reviewed future observer must detect every write, write
length, seek/append/truncate, copy, generated-cache/config read, symbol-table
resolution, missing-symbol/ignored-exception path and subprocess outcome.
A phase marked `done` in JSON alone does not establish that observation.

## Capacity, owners and overrides

An allocation has `id`, `component`, `kind` (`payload`, `overlay`, `dynamic`),
`start`, `end`, `basis` (exactly `independent_reservation`). Allocation extents
are disjoint. The selected original payload starts are CFRU 16 MiB and DPE
22 MiB. The CFRU payload **and every appended overlay allocation**, including
its alignment, must end at or before the DPE boundary. DPE must fit 32 MiB.
Overlays are 4-aligned, follow the aligned CFRU payload end and appear in
append order. Dynamic allocations are 4-aligned, disjoint from every other
allocation and independently reserved; `free_bytepatch` uses the original
minimum 256 B search capacity at/above its public search start. Zero/FF bytes
alone are rejected as a capacity or owner basis. A reserved allocation without
any corresponding observed write is rejected. Existing map-header repoints
are checked against their existing owner, not forced into the appended span.

An owner has `id`, `component`, `roles` (nonempty unique list), `start`, `end`,
`allocation` (ID or null), `basis` (`independent_link_and_input_map`). Physical
leaves never overlap, even under different IDs. An owner in a payload/dynamic/
overlay allocation is fully contained; owners without allocations are disjoint
from all allocations. Multiple semantic roles may share one physical owner,
for example a palette source that is an existing native palette asset; this
does not create a second overlapping physical owner.

Required roles include:

- Oak: 96 B record (4-aligned), 180 B eligibility bitmap, two distinct 28 B
  bridges and distinct front/cry consumers.
- Pickup: 64 B record (4-aligned), 28 B bridge and consumer.
- Evolution: 32 B record (4-aligned), consumer and 1440×16×8 B evolution rows.
- Native front/palette tables and assets; palette source, snapshot and
  repoints; learnset writer, allocator and rollback owners.

Records, bridges, bitmap, critical consumers and native/evolution tables must
be distinct physical leaves. Oak/Pickup/Evolution code/records belong to CFRU.
Asset and palette populations may have multiple disjoint leaves. Additional
active owners must be included; the required-role checklist is not a complete
native asset/code inventory. Every actual write needs an owner, including
writes subsequently overridden. Read-only adjacent data must be reserved too.
Missing required roles produce UNKNOWN. False size/alignment, overlap,
unauthorized write or pointer target produces FAIL.

An override has `earlier`, `later` (write IDs), exact intersection `start`,
`end`, `basis` (`reviewed_source_order`). Every overlapping nonmaterialization
write requires this explicit ordered edge. Earlier and later writes must have
the same physical owner/component; identical data never grants permission.
Unused, duplicate, reversed and incorrectly sized edges fail. Exact repeated
ranges also require earlier `after` == later `before`. Partial-overlap byte
provenance cannot be independently recomputed without the observer and remains
UNKNOWN at the original-observation gate. Expansion materializes the image;
payload materializes its owned allocation before later writes to its leaves.
These containment relationships are not arbitrary overwrite permissions.

## Remaining minimum follow-up before CFRU insertion

**UNKNOWN:** No trusted receipt producer is supplied. The original inserters
perform unrestricted file/subprocess operations, reuse generated caches and
can continue after missing symbols or caught allocation failures. Running
or monkeypatching them without an independently reviewed complete I/O and
failure observer would not safely establish full ownership. This three-file
implementation therefore does not execute or instrument private native runs.
The tests' receipt builder is synthetic data only and must never be used to
manufacture private acceptance.

The next single bounded decision is to approve a revision-bound **original
inserter observer/receipt producer**, with explicit allowed files and USER-only
execution, capturing original operations rather than replacing patch logic.
It must first support nonmutating validation of the selected original input
and full link/input-owner reservations, including the real CFRU overlay tail.
It must independently bind the actual clean complete source/config/tool run,
all generated objects/caches, resolved symbols, native link records and final
output; capture skipped/error paths; and reconcile each intermediate operation
and unchanged adjacent bytes. No new insertion is authorized by this document.
Only independently accepted D1 evidence can route a later insertion decision.

Native checks still needed include the installed Oak descriptor's version,
profile, identity and only mutable selector u16 at +92 (default 29), 1440-slot
bitmap contents/immutability, two bridges referencing the same record with
r0/r1 consumers, front-sheet/palette row tags and cry separation; Pickup E5,
29 u16 slots inside its record; Evolution consumer and field layouts; actual
Thumb relocations and all native data/asset capacities. #741 reproducibility
remains separate; no previous private test is rerun or promoted here.

## Public verification

```sh
python3 -B -m unittest discover -s 07_scripts/d1/tests -v
git diff --check
```

Fixtures contain invented numeric intervals and digests of synthetic strings.
No component test suites, native builds or protected inputs are needed.
Tests cover all original phase classes, boundary and one-byte overflow,
overlay append plus base-pointer writes, free-space reservations, physical and
critical semantic aliases, cache freshness, input/output/payload binding,
partial/failed runs, wrong sequence/count/scan origin, ordered overrides,
hook alignment/targets, missing owners, malformed JSON/types and output
sanitization. Native/observation hard gates cannot be set to PASS by a receipt.

Implementation verification: **50/50 synthetic unittest methods PASS**, zero
failures/errors/skips. No protected or native tests were run. The empty-input
CLI check printed only fixed UNKNOWN statuses and returned exit 2 as designed.
