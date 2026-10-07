# Public source profile schema v2

Schema ID: `cfru-dpe-tracker-source-profile`; integer `schemaVersion: 2`.
This schema supersedes the historical v1 source-data prototype. It is a public
source contract only. T2 Phase A's Lua adapter locks its complete canonical bytes
before decoding; production output/session validation remains unavailable. See
[T2 evidence](../../../docs/tracker/T2_PHASE_A.md) for the mock-only boundary and
Lua 5.4 execution evidence and separate Lua 5.1 / BizHawk NOT_RUN boundaries.

## Serialization and identity

JSON is UTF-8, sorted by object key, indented by two spaces and terminated with
one newline. Arrays retain source order or explicitly sorted numeric IDs.
Numbers are JSON integers in decimal; numeric strings, timestamps, host paths
and runtime addresses are absent. This avoids the pinned Tracker's string-as-hex
conversion ambiguity. Public hashes identify source text or canonical profile
content only, never protected artifacts.

`metadata.profileId` is `sha256:` plus SHA-256 of that serialization with only
the `profileId` member omitted. `metadata.generator.sha256` binds the exact
single generator source; source provenance binds each allowlisted input to its
component revision and raw-byte SHA-256. No moving branch names select inputs.
The product Workspace commit/tree and T0 contract commit/tree are separate.

`metadata.extensionCompatibility.workspaceCommit` / `path` / `gitBlob` bind
the historical extension at the immutable T0 contract, whose tree and extension
blob are verified. They do not constrain the extension implementation at later
Workspace HEADs. Current HEAD component Gitlinks and component checkout revisions
must still match every locked pin. Extension changes do not select source inputs
or certify runtime compatibility; `runtimeSchemaSupport` remains `UNRESOLVED`
until the separate T2 contract establishes acceptance.

`validate_profile(candidate, regenerated)` requires exact schema/version and
exact canonical equality with fresh generation from the locked inputs. It
rejects omitted/extra keys, changed pins, mappings, layouts, descriptors and
configuration even if a candidate recomputes its own hash. `--check` additionally
requires byte-identical serialization. No generic permissive JSON import is a
validator, and this function does not validate or accept runtime bindings.

## Required areas

| Area | Meaning |
| --- | --- |
| `metadata` | Schema, content identity, exact product/contract trees and component pins, generator/input provenance, configuration, name/numeric policies, extension compatibility boundary. |
| `counts` | Explicit source expressions and bounds, name-table locators/strides, mapped values and hole IDs. Item bounds include separate CFRU and DPE coverage. |
| `species`, `moves`, `abilities`, `items`, `types` | Ordered source ID slots: integer `id`, canonical `constant` (null for holes), `sourceExpression`, aliases with expressions, table name/labels/raw source text/truncation, and classification. |
| `tableCoverage` | Explicit initializer coverage for `gBaseStats` and `gBattleMoves`; absent species initializers and holes are implicit zero C rows, never supported data by inference. |
| `itemExclusions` | Every DPE-only Shiny slot, with ID, constant and `UNAVAILABLE` reason. These rows are not appended to the effective CFRU mapping. |
| `abilityNameOverrides` | Authoritative string catalog after the table terminator, source resolver and explicit `UNRESOLVED` contextual selection. Catalog presence does not imply applicability. |
| `layouts` | Target/endianness/pointer width, extraction proof and translation-unit hash, source record locators and declaration hashes, sizes/alignment and all field offsets/types. Bitfields add byte-relative `bitOffset` and `bitWidth`. |
| `limits` | Source-derived party size and maximum battler count with locators. |
| `addresses` | Source descriptors below. No resolved runtime address. |
| `capabilities` | Dependencies, applicability, contexts, confidence/reason, source-only flag and null sample epoch. All runtime confidence remains `UNKNOWN`. |
| `limitations` | Explicit boundaries on identity, mechanics, item exclusions and unmapped resources. |

Mapping `state` is `mapped`, `hole`, `sentinel` or `reserved`. A mapped ID is not
proof of supported mechanics, playable form, available art, or live data. Zero
sentinels and Egg are explicit. Missing `gBaseStats` rows have `baselineData:
UNAVAILABLE`. Type Mystery/Roostless/Blank are sentinel IDs; unnamed alignment
slots remain holes. Duplicate display names across forms are expected and do not
merge identities. Source string labels are retained literally, including legacy
abbreviations/mismatches; physical table position establishes the name-to-ID
association, never similarity of a macro name to a label.

Aliases within a header require an unambiguous expression target; unresolved
or conflicting duplicate IDs fail generation. For items the actual table's
`.itemId` selects the canonical spelling and must equal its positional index.
Reviewed cross-component Ogerpon/ability slot spellings carry explicit DPE
provenance and do not promise equivalent mechanics. Required count macros must
resolve; in particular ABILITIES_COUNT comes from CFRU, where it is actually
defined, not from a maximum-ID fallback in DPE.

String conversion follows the locked converter's fixed maximum length and
FF-fill/terminator convention without executing that converter. `sourceText`
retains original text/tokens; `name` is the decoded, width-limited table spelling.
Typographic quote aliases in the source charmap display as ASCII quotes. Unknown
escapes/glyph bytes and ambiguous charmaps fail. The dynamic ability catalog is
not part of the 255-ID mapping or a selectable table extension.

## Source addresses and ABI

Descriptors require `kind`, `source`, `domain`, `widthBytes`, `indirection`,
`runtimeAddress` and validation requirements. Source-backed numeric constants
add `sourceAddress`; unresolved bindings carry a reason instead.

- `fixed-symbol`: public linker declaration; indirection 0. It is still unbound
  to any loaded session. Array widths describe the read unit, not row size.
- `pointer-slot`: source explicitly dereferences a 32-bit slot; indirection 1.
  `sourceAddress` locates the slot, not the pointee/table.
- `repoint-anchor`: an insertion/repoint reference. Indirection is null because
  this is not permission to perform a memory read or chase a pointer.
- `UNRESOLVED`: no proven descriptor chain to a target. Indirection is null.

ROM constants must be aligned within the GBA ROM domain; fixed RAM symbols must
fit EWRAM and their read alignment. All `runtimeAddress` values are `UNRESOLVED`,
even where public source gives a numeric constant. T2 must validate output
binding and the complete dependency set before any capability can activate.
Trainer B is an ExtensionState field, not an independently inferred vanilla
address. The old BPRE base-stat address is not chosen over the repointed table.

Layouts are generated by Clang's `thumbv4t-none-eabi` target from full extracted
record declarations plus source-checked primitive types/constants. Syntax-only
stdin compilation emits a textual layout, never a game build or native ABI
measurement. Every declaration member must appear in the extraction; reviewed
size/key-offset assertions fail on drift. The exact compiler version is test
execution evidence, not variable profile content: a compiler producing different
layout facts cannot pass committed-profile comparison. Target ABI facts remain
conditional on those declarations/ABI; private output compilation and live
acceptance belong to later gates.
