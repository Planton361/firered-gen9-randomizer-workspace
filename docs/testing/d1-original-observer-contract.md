# #727 — Original-inserter observation and independent byte verification

**CONFIRMED USER DECISION:**
[Approval 6385443092](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/727#issuecomment-6385443092)
authorizes this bounded source implementation. Base:
`99842eb59ec3a775c330cb254454200c571b44dd`; branch:
`audit/727-d1-original-observer`. Original Workspace only, one writer, no
component/Gitlink changes. Live preflight confirmed #727 sole Doing/P0,
Component Delivery; known CFRU/UPR checkout differences remain unstaged.

**CONFIRMED CURRENT STATE — source/synthetic evidence only:** The helper
executes the exact original entry points in a Linux bubblewrap sandbox,
redirects their supported Python file operations into RAM, streams private
observations and independently reconstructs every recorded I/O effect. It can
compare those results with existing selected outputs, verify exact linked
payload bytes, check critical physical symbol reservations and check installed
Oak record/bridge/bitmap structure. It does not run a native DPE/CFRU build.

**UNKNOWN / STOP:** No fresh-build execution history, complete source-derived
native asset/learnset owner census, C consumer semantics, relocation history or
#741 reproducibility proof is supplied by this implementation. These gates
remain UNKNOWN even after successful live recomputation. `D1_ALL` never becomes
PASS here. This limitation is deliberate, not a claim that matching output or
self-declared metadata constitutes complete D1. CFRU production insertion and
UPR Stage B remain unauthorized.

## Exact six-file allowlist

1. `07_scripts/d1/observe_original_inserters.py`
2. `07_scripts/d1/tests/test_observe_original_inserters.py`
3. `07_scripts/d1/validate_owner_write_sets.py`
4. `07_scripts/d1/tests/test_validate_owner_write_sets.py`
5. `docs/testing/d1-owner-validator-contract.md`
6. `docs/testing/d1-original-observer-contract.md`

The existing receipt validator retains its previous semantics, including all
63 regression tests and native UNKNOWN gates. Its new pure-byte/ELF helpers
are called by the live observer; its receipt CLI gains no trust switch.

## USER-ONLY invocation

USER independently prepares a private local plan and an **existing ignored
scratch directory inside the original Workspace**. Set `D1_OBSERVER_PLAN`
locally to that plan filename, then run from this Workspace:

```sh
python3 -B 07_scripts/d1/observe_original_inserters.py --plan "$D1_OBSERVER_PLAN"
```

Linux, Python 3 with `Path.is_relative_to`, working bubblewrap user namespaces,
Git and the original inserters' native preflight tools are required. The helper
neither installs nor substitutes tools. Missing isolation, unavailable tool,
unsupported operation/layout, exhausted resource budget or absent proof yields
UNKNOWN/STOP. Existing selected DPE output must equal the existing CFRU input;
existing selected outputs are required for the reproduction comparison. The
command never creates or replaces those selected originals. A stale/mismatching
existing output is FAIL, not permission to overwrite it.

No plan is needed to inspect the fixed status schema: running without arguments
prints UNKNOWN statuses and opens no private artifact. Do not pass private
artifacts to Codex or upload plans, traces, paths, hashes, maps, symbols, native
outputs, tool logs, presets or images. Only fixed status lines may be returned.

The plan is JSON with exactly `schema` (integer **2**), `scratch` (relative path
to the existing ignored directory) and `ownership`. `ownership` contains:

- `config`: the private scoped review's configuration digest.
- `allocations`, `owners`: the physical reservations from the
  [receipt contract](d1-owner-validator-contract.md#capacity-owners-and-overrides).
- `overrides`: explicitly reviewed edges, with the exception below.

No `fresh`, `native_pass`, trusted hash, receipt or acceptance flag is accepted.
An empty/incomplete owner map stops; the helper does not invent reservations
from free bytes. User-provided reservations are *obligations to cross-check*,
not evidence of a complete native owner census. Oak/Pickup/Evolution records,
bridges and consumers must additionally match actual final ELF symbols and
sizes. Other source-derived native reservations remain a concrete missing gate.

Observed write IDs are `dpe_N` / `cfru_N`, zero-based over **actual ROM writes**
(including expansion/payload/no-op writes). These differ from guessed final
diffs. A schema-2 cross-override binds the **entire actual journal write event**
using `write_binding(event, component)` from the validator, with the same scoped
review reference, decision digest, exact source revisions, config and physical
owner rules as schema 1. Existing schema-1 write digests cannot be reused.
USER retains first-run private journals to prepare/review exact scoped edges,
then reruns the RAM-only observation if that review supplies missing evidence.
A generic source-order edge never grants DPE → CFRU permission. Every actual
intersection needs an edge; every foreign-write byte needs approved coverage.

## Isolation and execution boundary

The internal worker entry additionally checks read-only mount flags for the
host/component and a live invocation nonce before executing anything native;
it cannot be used as a CLI bypass around the isolation prerequisite.

The live command checks exact component HEADs:

| Component | Revision |
| --- | --- |
| CFRU | `196058edbc2b8b7d8c725b715b1f967ba60f5c83` |
| DPE | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| UPR | `e1127cfde58af359e458f8d6a19339f3db3c8589` |

It checks tracked source drift and the exact public inserter byte identities.
Line-to-phase classification is valid only for those exact public scripts.
A changed script is rejected rather than guessed or patched. No build-profile
rewriting, source checkout switch, automatic Gitlink reconciliation or cache
reset is performed. Public source identity is narrower than full build/config
provenance; ignored inputs and historical compile flags remain unproved.

Bubblewrap mounts the host read-only, creates new namespaces without networking,
and permits disk writes only in the unique ignored evidence directory and a
private RAM `/tmp`. The original `BPRE0.gba`, `test.gba`, compiled outputs,
component files and caches stay read-only on disk. Original `shutil.copyfile`
initializes a RAM image. Only virtual `test.gba`, `generatedrepoints` and
`offsets.ini` are writable by the insertion Python process. Other write paths,
foreign path/symlink aliases, file descriptors and unsupported modes stop.

Both original `main` entry points execute, DPE first, CFRU second. The original
CFRU source-contract import and linked-output audit remain in the execution
path. The latter may invoke its original target-compiler/objcopy **preflight**
in private temporary storage; this is not a full component rebuild. The driver
allows only the original bounded symbol commands, read-only Git queries and
that exact preflight subprocess. Original native child stdout/stderr is
captured privately, never forwarded. Unsupported subprocess effects latch STOP
even if the original catches the exception. An original missing-symbol print,
unhandled exception, failed subprocess or caught allocation error cannot
silently become a successful observation.

## Independent recomputation and private evidence

A unique `d1-*` directory is retained under the configured ignored scratch.
It contains worker configuration, a streaming `operations.jsonl`, RAM output
and a private completion report for each stage. Directory names, hashes and
contents are never printed. These are private scratch **artifacts**, not a
second source workspace. No source tree is copied. No private path is staged.

The observer records actual open/read/seek/write/truncate/close/copy effects,
write bytes and preimages, original caller/phase, dynamic `FindFreeSpace`
results and subprocess outcomes. Unchanged writes remain separate events.
Original cache reads and cache/offset writes are observed; they are not silently
regenerated to obtain a different path. Snapshot hashes are checked against
fresh reads of the original files after execution. A changed/stale snapshot,
wrong selected input, incomplete report or stale invocation nonce is rejected.

A separate `JournalVerifier` implements its own byte store and handle positions.
It reads the actual snapshots, recomputes all read results, seeks, preimages,
copy/expansion/append/truncation effects and output bytes. The RAM backend counts
and hashes real writes separately from journal emission. Recomputed count and
ordered-byte binding must match that live backend, detecting missed/doubled
unchanged writes too. The command always creates a **new live invocation**;
it has no mode that accepts an arbitrary existing report/receipt as proof.

Physical capacity checks include CFRU payload plus aligned appended overlays,
DPE's 22 MiB boundary and the 32 MiB image ceiling. Free-space results must fit
independent dynamic reservations, including a 3,778,560-byte request; 00/FF
content supplies no owner proof. Encoded pointer/hook/wrapper destinations must
land in declared owners, with widths and Thumb alignment checked where known.
Missing owners, destructive aliases, wrong order and unreviewed intersections
stop. Bulk materialization and non-writing seeks are distinct from overrides.

Final-link checks parse bounded ELF32 little-endian ARM executable bytes,
resolve unique named symbols, compare the actual single loadable `.text`
payload and expected insertion origin, and check installed bytes. Unsupported
multi-section/LMA layouts remain UNKNOWN. The Oak check verifies the 96 B
record, default selector, 180 B bitmap from pinned source directives, exact
28 B bridge instruction/literal structure, Thumb target flags and distinct
consumer/record/bitmap intervals. Critical declared owners must equal actual
linked symbol intervals. Marker matches or receipt-supplied hashes cannot
replace these comparisons. These are structural checks, not C semantics or
relocation-history acceptance.

## Status and resource contract

Only fixed `PASS|FAIL|UNKNOWN` values appear under these keys:

```text
D1_SANDBOX D1_PUBLIC_SOURCE_IDENTITY D1_ORIGINAL_EXECUTION
D1_IO_RECOMPUTATION D1_CAPACITY D1_DECLARED_OWNER_CHECKS
D1_REVIEWED_OVERRIDES D1_LINK_IMAGE D1_OAK_LINK_SHAPE
D1_INPUT_CHAIN D1_OUTPUT_REPRODUCTION D1_CACHE_FRESHNESS
D1_SOURCE_CONFIG_BUILD_PROVENANCE D1_FULL_NATIVE_OWNERSHIP
D1_ABI_RELOCATION_SEMANTICS D1_DPE_REPRODUCIBILITY D1_ALL
```

Exit 1 is FAIL; exit 2 is UNKNOWN/STOP; exit 0 is unavailable. Detected
contradictions fail. Missing/unsupported evidence stops UNKNOWN. No errors,
tracebacks, raw symbols, commands, paths, offsets or subprocess text are emitted
by the public CLI. Earlier completed narrow checks do not promote later gates.

Limits are explicit: a 1.5 GiB isolated-process address-space ceiling, 512 MiB
virtual-file/snapshot budgets, 128 MiB retained
write-history budget, 100 million journal operations, 8 GiB journal data,
128 MiB per journal record and two hours per isolated stage. Journals are
streamed, not sampled or truncated. Sparse page indexing bounds overlap checks;
large limits are not promises of host capacity. Resource exhaustion stops
UNKNOWN. No silent loss of events or false completeness is permitted.

Cache freshness may PASS only when no pre-existing generated-repoint cache was
used. Existing caches remain UNKNOWN without independent fresh-run binding;
matching output does not certify cache freshness. Fresh compile history, full
native ownership, ABI/relocation semantics and DPE reproducibility always remain
UNKNOWN here. Therefore even all implemented checks passing leaves D1_ALL
UNKNOWN. #741 differences are not waived.

## Public tests and next concrete insertion condition

Codex ran only ROM-free synthetic tests, including the original 63 regressions,
independent ELF/ABI mismatch tests, a synthetic original worker entry, every
write phase, missed/double no-op writes, denied effects, reviewed/unreviewed
cross-overrides, protected owners, overlay boundary, dynamic capacity, stale
snapshot/nonce and sanitized failures. No real original inserter, sandbox,
compiler, private binary, ROM or native build was executed by Codex.

```sh
python3 -B -m unittest discover -s 07_scripts/d1/tests -v
git diff --check
python3 07_scripts/bootstrap/check_git_safety.py
```

The next concrete condition for production CFRU insertion is independent
CONTROL review of this exact source revision **and** USER-only evidence on the
selected stack covering all missing gates: source/config/tool → fresh generated
objects/cache → link identity, complete source-derived native owner inventory
(including front/palette/learnset/Pickup/Evolution owners), resolved relocation
and consumer ABI semantics, and #741 reproducibility disposition. The observed
RAM write-set/selected-output checks and every scoped override must then be
accepted for that exact identity. A separately scoped independent acceptance
path is still required for these missing gates; neither this command nor a
receipt can certify them. Until then: `D1_ALL=UNKNOWN`, no production insertion,
no UPR gameplay-test promotion and no merge/pin authorization.

Verification result: **90/90 synthetic test methods PASS**, zero failures,
errors or skips (63 receipt regressions, 6 independent link checks, 21 observer
checks). No native/USER-only test was run by Codex.
