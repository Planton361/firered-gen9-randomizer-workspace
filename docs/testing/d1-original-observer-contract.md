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

## Original observer's six-file scope (historical implementation authority)

1. `07_scripts/d1/observe_original_inserters.py`
2. `07_scripts/d1/tests/test_observe_original_inserters.py`
3. `07_scripts/d1/validate_owner_write_sets.py`
4. `07_scripts/d1/tests/test_validate_owner_write_sets.py`
5. `docs/testing/d1-owner-validator-contract.md`
6. `docs/testing/d1-original-observer-contract.md`

The existing receipt validator retains its previous semantics, including all
63 regression tests and native UNKNOWN gates. Its new pure-byte/ELF helpers
are called by the live observer; its receipt CLI gains no trust switch.

## Minimal discovery bootstrap — #727

**CONFIRMED USER DECISION:** The bounded follow-up implements the route in
[CONTROL 6403396358](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/727#issuecomment-6403396358),
on `audit/727-d1-owner-plan` from exact
`2bc8e468ec315575e3540f5f3190abb61cb9a52f`. Only this contract, the existing
observer and its tests change. No separate generator or validator is needed.
Live preflight found #727 the sole Doing/P0, Component Delivery; #726 and
#741 Ready. The documented CFRU/UPR checkout differences are preserved.

**CONFIRMED CURRENT STATE — implementation decision:** Complete ownership is
not required for an isolated observation. The original RAM worker and separate
`JournalVerifier` already reconstruct writes without granting ownership.
`--discover` omits plan-dependent `OwnerChecks` and the CFRU production-output
comparison, while retaining source and script identities, selected input chain,
read-only bubblewrap, nonce, resource
limits, snapshot freshness, backend count/binding, DPE selected-output
reproduction and link/Oak structural checks on the reconstructed images.
A failed or unsupported observation stops;
partial journals never become a completed candidate plan. No native build is
repeated. Native compatibility of this new path remains USER-ONLY / NOT_RUN.

**CONFIRMED USER DECISION — same-contract repair:** Following
[CONTROL 6403661086](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/727#issuecomment-6403661086),
the repair starts at `36e5154057415241b87f68c7d8b64c0cf5ddf177` on the same
branch and three-file scope. Pre-insert discovery must not require a product
output that has not yet been authorized or produced. DPE's existing output is
still compared with both its RAM replay and CFRU's selected input. For CFRU
discovery, the separate `JournalVerifier` reconstructs the image and compares
it with the worker RAM output; those verified bytes feed all subsequent ELF,
candidate and Oak checks. Existing CFRU `test.gba` is never read, required,
created or replaced by discovery, including when it is absent or stale.
`D1_OUTPUT_REPRODUCTION` stays UNKNOWN in discovery: RAM agreement does not
prove final productive CFRU output provenance. `--plan` retains both existing
selected-output comparisons and all previous strict owner/override checks.

### USER-ONLY Fish/Linux sequence

1. USER locally sets `D1_SCRATCH` to the **already existing**, ignored scratch
   directory relative to the original Workspace, inside `.local/`. No plan is
   required. From the Workspace root, run:

   ```fish
   python3 -B 07_scripts/d1/observe_original_inserters.py --discover "$D1_SCRATCH"
   ```

   Existing source/compiled inputs, selected DPE output and CFRU input are still
   required; a selected CFRU production output is not a discovery prerequisite.
   Missing originals, tools or isolation yield UNKNOWN; mismatches yield FAIL.
   The command creates only a unique private `d1-*` evidence directory under
   that scratch. It never chooses or creates another scratch workspace.

2. USER privately reviews the new directory's `candidate-plan.json` and
   `candidate-census.jsonl` against its two stage journals/reports and independent
   public source + local link/input evidence. The census preserves ordered
   `dpe_N`/`cfru_N` writes, including unchanged and zero-length writes, source
   lines/functions, exact operation bindings, dynamic free-space requests and
   every intersecting write pair. Bulk expansion/payload intersections are
   marked as materialization, without granting an override. Full read/seek/
   copy/truncate/cache operations and actual bytes remain in the original
   `operations.jsonl`; dynamic repoints and map-overlay writes are observed,
   not guessed from final differences. The final `census_complete` record
   appears only after both stages' independent recomputation and comparisons.

   The candidate contains only linked payload extents and public named roles
   resolved from actual sized ELF symbols and compared with verified image bytes
   (the independently reconstructed RAM image for CFRU discovery):
   the existing eleven Oak/Pickup/Evolution bindings, plus DPE
   `gMonFrontPicTable`, `gMonPaletteTable` (1440 × 8 B each) and
   `gEvolutionTable` (1440 × 16 × 8 B). Missing symbols remain missing. No owner
   for an asset, patch, dynamic allocation or map overlay is invented.
   `ownership.config` and **all** candidate `basis` fields are `null`;
   `overrides` is empty, even for identical writes. Observed placement supplies
   no reservation or permission. Passing this candidate unchanged to `--plan`
   stops UNKNOWN before any worker executes.

3. An independent USER-local source/link/input review must produce a separate
   reviewed schema-2 plan in the **same ignored scratch**. Review all physical
   leaves, capacity and protected ranges, not only candidate symbols; add the
   missing reservations/owners only when independently supported. Supply the
   actual scoped configuration binding and the contract's independent bases
   only after that review. For each nonmaterialization intersection, review
   exact original source behavior and both complete operation bindings; a
   DPE→CFRU edge additionally requires the narrow shared-patch owner, exact
   range, source/config binding and independent decision defined below. Never
   mechanically replace `null` fields or turn census rows into permissions.

   **POST-INSERT only:** After a separately authorized productive insertion has
   supplied a selected CFRU output, USER locally sets `D1_OBSERVER_PLAN` to
   that independently reviewed plan and runs the existing checking path:

   ```fish
   python3 -B 07_scripts/d1/observe_original_inserters.py --plan "$D1_OBSERVER_PLAN"
   ```

   This requires both selected outputs, performs a fresh RAM observation, no
   build, and rechecks the complete write set, actual link reservations, exact
   override bindings and equality of both RAM images with selected outputs.
   An absent CFRU output stops UNKNOWN; a stale/mismatching one fails. A candidate
   or edited receipt alone cannot authenticate the independent review or
   satisfy the native gates. Missing proof stays UNKNOWN. No private artifact
   or its path, map, hash or log may be returned to Codex/CONTROL; share only
   the fixed status lines.

The **PRE-INSERT** evidence is the isolated discovery, DPE output/input-chain
comparison, independent CFRU RAM reconstruction, ELF/Oak structural checks and
independent owner/reservation/override review. It does not certify a productive
CFRU output. `--plan` is a **POST-INSERT** output comparison, not a circular
prerequisite for creating that output. The minimal remaining user-decision
gate before productive insertion is explicit acceptance of the exact pre-insert
evidence after the native/ABI/provenance/#741 prerequisites are independently
resolved, followed by separate insertion authorization. Discovery never grants
that authorization or waives unresolved proof; this helper cannot close the
full pre-insert gate.

Concrete missing-proof categories and public source starting points:

| Status (UNKNOWN until independent proof) | Required USER-local evidence |
| --- | --- |
| `D1_RESERVATION_REVIEW` | Both selected `scripts/insert.py`, patch lists, CFRU `mapobjectoverlays` and actual input map structure; independent bounds/exclusivity for payloads, each free-space request, appended overlay and protected patch leaf. FF/00 search results are insufficient. |
| `D1_ASSET_OWNER_CENSUS` | DPE `src/Front_Pic_Table.c`, `src/Palette_Table.c`, actual selected pointers and complete asset extents/aliases; UPR `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` palette source/snapshot/repoint reservations. A table symbol is not its pointed-to asset inventory. |
| `D1_LEARNSET_OWNER_CENSUS` | DPE `src/Learnsets.c`, CFRU `src/learn_move.c`, and the selected UPR handler's learnset writer/allocator/rollback paths with physical input/output reservations. |
| `D1_REVIEWED_OVERRIDES` | Exact pending intersections, original source lines, same physical owner, scoped independent source/config decision and complete operation bindings; no generic source-order or identical-byte waiver. |

These category keys do not certify evidence authentication. The first three
stay UNKNOWN in this bounded helper, as do all four pre-existing hard native
gates. `--discover` also leaves `D1_CAPACITY`, `D1_DECLARED_OWNER_CHECKS` and
`D1_REVIEWED_OVERRIDES`, plus `D1_OUTPUT_REPRODUCTION`, UNKNOWN.
Only completed observation and candidate-file
creation can set `D1_DISCOVERY=PASS` / `D1_CANDIDATE_PLAN=PASS`; those statuses
never mean the candidate is an accepted ownership plan. An unsupported class,
budget exhaustion or missing prerequisite prevents those PASS values.

## USER-ONLY invocation

For the ownership-checking path, USER independently prepares a private local
plan and an **existing ignored scratch directory inside the original Workspace**.
Set `D1_OBSERVER_PLAN`
locally to that plan filename, then run from this Workspace:

```sh
python3 -B 07_scripts/d1/observe_original_inserters.py --plan "$D1_OBSERVER_PLAN"
```

Linux, Python 3 with `Path.is_relative_to`, working bubblewrap user namespaces,
Git and the original inserters' native preflight tools are required. The helper
neither installs nor substitutes tools. Missing isolation, unavailable tool,
unsupported operation/layout, exhausted resource budget or absent proof yields
UNKNOWN/STOP. Existing selected DPE output must equal the existing CFRU input;
in this `--plan` path both selected outputs are required for reproduction. The
command never creates or replaces those selected originals. A stale/mismatching
existing output is FAIL, not permission to overwrite it.

No argument is needed to inspect the fixed status schema: running without arguments
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
D1_DISCOVERY D1_CANDIDATE_PLAN D1_RESERVATION_REVIEW
D1_ASSET_OWNER_CENSUS D1_LEARNSET_OWNER_CENSUS
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
RAM write-set, DPE selected-output/input-chain checks and every scoped override
must then be accepted for that exact identity. Final productive CFRU output
provenance is a separate post-insertion check, not a pre-insert discovery
prerequisite. A separately scoped independent acceptance
path is still required for these missing gates; neither this command nor a
receipt can certify them. Until then: `D1_ALL=UNKNOWN`, no production insertion,
no UPR gameplay-test promotion and no merge/pin authorization.

Verification result: **90/90 synthetic test methods PASS**, zero failures,
errors or skips (63 receipt regressions, 6 independent link checks, 21 observer
checks), before this bootstrap. Bootstrap verification: **100/100 PASS**, including
all previous 90 and ten discovery methods (with parameterized failure cases).
Coverage adds the shared live driver with synthetic RAM inputs, no-op/zero-write
identity, dynamic reservation nonauthorization, exact pending conflicts,
overlay/phase boundaries, missing symbols, resource limits, candidate rejection,
source/ignore/input/output/nonce/journal/worker/isolation failures, actual
synthetic scanner tracing and CLI sanitization.
No native/USER-only test was run by Codex. D1 native, ABI, provenance and #741
reproducibility gates remain UNKNOWN; `CFRU_INSERTION_READY=NO`.

Same-contract output-dependency repair: **107/107 synthetic methods PASS**,
including the previous 100 and seven new regressions: discovery with absent or
stale CFRU output (zero reads/overwrites), DPE replay/output mismatch, CFRU ELF,
journal and Oak failures, and unchanged `--plan` behavior for missing, stale
and matching CFRU output. Discovery's production-output status remains UNKNOWN
even when all narrow replay checks pass. No native/private run was performed.
