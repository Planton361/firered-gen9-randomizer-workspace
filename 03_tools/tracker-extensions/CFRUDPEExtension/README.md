# CFRU/DPE Gen9 Tracker Extension

Workspace-owned extension for the standard Ironmon Tracker, without a Tracker
fork or NatDexExtension dependency. The normative architecture and lifecycle
contract are in [the Tracker docs](../../../docs/tracker/README.md) and
[PROFILE_CONTRACT.md](../../../docs/tracker/PROFILE_CONTRACT.md).

## T2 Phase A — Issue #691

The extension now has a fail-closed early guard and a detached, in-memory mock
transaction adapter. Production activation is always denied: actual output /
session identity remains `UNKNOWN`. No local manifests or emulator reads are
performed by the production instance. The mock factory refuses Tracker/emulator
hosts and can publish only `TEST_ONLY`, never verified live data.

**Source checks PASS; Lua mock/syntax checks NOT_RUN on this Mac.**
`CFRUDPE_EXTENSION_PROFILE_MOCK_GUARD_READY` is not yet established. Full behavior,
ownership/rollback rules, the persistent unload/restart stop guard and commands
are recorded in [T2_PHASE_A.md](../../../docs/tracker/T2_PHASE_A.md).

For future local installation, keep `profile_sha256.lua` alongside the extension
Lua file; `data/source-data.json` remains the unchanged public T1 profile. Do not
activate a real session as a Phase A test. The old example manifests remain inert.

## T1 source profile — Issue #690

**CFRUDPE_TRACKER_PROFILE_READY — source/synthetic evidence only.**
The existing generator now produces schema v2 from the locked public CFRU/DPE
sources. This does not establish BizHawk readiness, a loaded-output identity,
Runtime addresses, extension activation, or Tracker UI compatibility.

| File | Role |
| --- | --- |
| `data/source-data.json` | Deterministic public profile: exact pins, input hashes, mappings, authoritative baseline names, bounds, ARM layouts and unresolved runtime dependencies. |
| [SCHEMA.md](SCHEMA.md) | Concrete schema v2 semantics and validation rules. |
| `CFRUDPEExtension.lua` | T2 source-v2 guard and isolated mock lifecycle candidate; production always unsupported. Lua behavior awaits actual mock execution; live data adapters remain T3–T5 work. |
| `data/*.example.json` | Historical prototypes, not valid v2 profiles or runtime acceptance templates. |

`game-addresses.local.json` and `tracker-overrides.local.json` remain ignored,
local-only future inputs. T1 does not inspect or generate these files, execute
the local address/override helpers, or access protected game/build artifacts.
No source-only check authorizes a real Tracker session.

## Reproduce and check

Requirements: Python 3, Git, and Clang supporting the ARM target
`thumbv4t-none-eabi`. Clang performs a syntax-only check of source-extracted
standalone declarations passed through stdin. It emits no object, executable,
ROM or game build, and does not use native macOS `sizeof` as GBA evidence.

From the Workspace root on an approved non-main branch:

```sh
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py --check
python3 -m unittest discover -s 07_scripts/tracker -p 'test_generate_cfru_dpe_source_data.py' -v
```

An alternate compiler executable can be selected with `--clang`. Output is
written only after all extraction/ABI checks succeed; `--check` writes nothing.
`--output /tmp/cfru-dpe-source-profile.json` can be used for a second independent
public-profile output. No local address manifest belongs in that argument.

The generator reads an explicit allowlist of public text files via
`git show <locked-commit>:<path>`. It verifies product/contract trees, current
Workspace Gitlinks and component checkout HEADs. Local component file edits are
not generator inputs: the profile describes committed source only. It neither
scans worktrees nor runs component build/string-conversion scripts. Changing a
pin/configuration requires a reviewed lock update, not an automatic fallback.

The generator SHA-256 identifies its exact source implementation, avoiding a
self-referential output-commit ID. Profile identity hashes the canonical JSON
without `metadata.profileId`. The locked product commit/tree remain distinct
from the T0 contract merge. The later T1 delivery commit is PR evidence, not a
claim that the locked product was runtime-tested again.

## Confirmed source facts

- Bounds: species 1440, moves 992, abilities 255, effective CFRU items 779,
  types 25. These include sentinels/holes and are not playable-content counts.
- Names come from physical string-table rows or `gItemData.name`, with the source
  converter's fixed widths, explicit truncation, escapes and glyph encoding.
  Examples include `Nidoran♀`, `Flabébé`, `PsychicNoise`, `Boost Energy` and
  `Stellr`; names are not normalized macro labels or expanded official names.
- Species IDs 252–276 have name-table slots but no constants. Shadow Warrior
  (706), Zygarde Cell (835) and Zygarde Core (836) have constants but no explicit
  `gBaseStats` initializer; their implicit zero data is `UNAVAILABLE`.
- Ogerpon slots 1426–1429 have different CFRU color and DPE Terastal spellings.
  Both are preserved at the same IDs without promising form-transition behavior.
  DPE `ABILITY_UNUSED` at 77 is CFRU `ABILITY_LINGERINGAROMA`.
- The 779 positional CFRU item rows match their `.itemId` and active constants
  with `EXPANDED_NEW_ITEMS` enabled and `UNBOUND` disabled. Free-space slots
  776–778 are reserved. DPE-only Shiny slots 779–798 have no CFRU item rows and
  are excluded. Inactive UNBOUND names are not aliases of effective items.
- Ability macro aliases have explicit target expressions. The 255 baseline name
  rows are followed by `NAME_LAST_ABILITY` and a separate dynamic-name catalog.
  `GetAbilityNameOverride` depends on species/effective types and other context;
  choosing the first alias or the baseline table name cannot establish the live
  name. That resolution remains T3 work.
- ARM layout sizes: Pokemon 100, BattlePokemon 88, BattleMove 12, BaseStats 28,
  Trainer 40, TrainerMonItemCustomMoves 32, Item 44 bytes. `BattleMove.split`
  is byte 10, BaseStats hidden ability byte 26, and Pokemon hidden-ability bit
  is byte 75 bit 7. Pointer-containing records use 4-byte target pointers.
- Public linker symbols, dereferenced pointer slots and repoint anchors are
  separate descriptors. Even a source-fixed symbol has `runtimeAddress:
  UNRESOLVED`; local output/session validation is still required.

## Verification and remaining boundaries

The focused suite covers parsing/aliases/holes/sentinels, authoritative names,
Gen1/mid-dex/Gen8/Gen9/regional identities, six synthetic party slots, battle and
move-category bytes, item exclusions, invalid/missing source facts, wrong
schema/revisions, layout/address mutations and byte-identical regeneration.
The ABI derivation uses full declarations, verifies every field was extracted,
compares CFRU/DPE BaseStats declarations and asserts reviewed key sizes/offsets.
It is source evidence under the declared ARM ABI, not proof of a private output
or its compiler flags.

**UNKNOWN / UNRESOLVED:** loaded-output binding, effective randomized values,
contextual ability naming, session identity/epochs, safe battler/party context,
Trainer A/B runtime binding, resource/UI fidelity and runtime ABI acceptance.
No capability is marked runtime-ready. B1 remains `PENDING_LINUX_HOST / NOT_RUN`;
T2 activation and subsequent runtime gates retain their own authorization and
acceptance requirements.
