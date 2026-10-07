# T3 #692 — Mac-first source / synthetic party decoder

**CONFIRMED SOURCE/SYNTHETIC EVIDENCE:** bounded Phase A candidate on
`feature/692-source-party-decoder-mock`, based on accepted Workspace main
`35576d3c8e6a219ee1da3e72197f46d31ac89c49`, tree
`7b190faac9b248c0f78aa9e45259899d5bbf0f22`. The
[updated #692 contract](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/692)
waives T2 runtime acceptance only for this detached preparation.

Review target: `CFRUDPE_TRACKER_PARTY_DECODER_MOCK_READY`. Tests support a
source/fixture candidate; the marker requires review/acceptance. This does not
establish `CFRUDPE_TRACKER_DATA_FIDELITY_READY` or close #692.

## Implementation and source identity

The detached [Lua module](../../03_tools/tracker-extensions/CFRUDPEExtension/source_party_decoder.lua)
is never loaded by `CFRUDPEExtension.lua`. That entire production-denied file,
its SHA helper, the T1 generator/profile and every component Gitlink remain
byte-identical to the accepted main basis. No Tracker-core changes are made.

`newMock(publicJsonText, publicSourceTexts)` hashes the complete accepted T1
serialization before an internal restricted JSON parser consumes it. Caller
profile objects, names or JSON-decoder callbacks cannot substitute facts.
Wrong schema/pin/content fails construction with an `UNKNOWN` diagnostic and
no usable decoder. Only exact previously hashed immutable strings are cached;
profile/mapping objects are private and returned values are fresh copies.

| Accepted source binding | Value |
| --- | --- |
| T1 schema | `cfru-dpe-tracker-source-profile`, version 2 |
| Public JSON SHA-256 | `8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981` |
| Profile ID | `sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75` |
| CFRU | `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2` |
| DPE | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| UPR-FVX | `4670a5413104ec02bc08c09ff584470a8a6cb7bd` |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |

Supplemental interpretations consume only five public texts, checked against
the unchanged T1 `metadata.inputs` hashes/revisions:

- `DPE:src/Base_Stats.c`: declared baseline types and ability assignments.
- `CFRU:src/Tables/battle_moves.c`: baseline type, power, accuracy, PP and
  `split` category, with T1 configuration conditionals selected explicitly.
- `CFRU:include/battle.h`: category constants.
- `CFRU:include/constants/battle.h`: primary status masks / toxic counter.
- `CFRU:include/pokemon.h`: level limit; party ABI still comes from T1.

No supplemental public profile/schema, generated file, new identity, runtime
address or output binding is introduced. The Python runner retrieves only these
allowlisted committed source objects through existing `LockedSources`. Its
independent Python baseline assertions exist in memory only.

## Detached API and confidence

`resolve(kind, id)` covers the T1 species, moves, abilities, items and types
catalogs. `speciesBaseline(id)` adds source types/ability assignments;
`moveBaseline(id)` adds source numeric move fields. Form identities retain
internal IDs/constants/aliases even when table names are equal. Truncated and
abbreviated source names remain literal; neither a name nor an assignment proves
modern mechanics or form support.

`decodeMock(syntheticBytes, syntheticCount)` accepts exactly six 100-byte CFRU
rows as a Lua string and an integer count 0–6. It requires a consistent occupied
prefix and `SPECIES_NONE` outside that prefix. It does not infer count from a
missing value. Fixtures use independent literal offsets; production decoding
uses the accepted T1 layout. There is no XOR or substructure shuffling.

| Direct Pokemon surface | GBA source layout / behavior |
| --- | --- |
| Species / held item | Offsets 32 / 34, little-endian u16 |
| Moves / current PP | Offsets 44 / 52, four u16 / four u8 |
| Hidden ability / Egg | Byte 75, bits 7 / 6; separate from selected ability |
| Primary status | Offset 80, u32; explicit masks, toxic counter and locked FROSTBITE configuration |
| Level | Offset 84, u8, source limit 1–100 |
| HP / max HP | Offsets 86 / 88, u16; zero current HP is valid, maximum must be positive and at least current HP |

Each field has `confidence`, `value`, `reason`, `provenance`,
`evidence: TEST_ONLY`, and `liveConfidence: UNKNOWN`. `VERIFIED` here means an
exact public source fact or validated synthetic field, never verified live
memory. Source-baseline data is explicitly marked through scope/provenance.

- `VERIFIED`: supported mapping/direct synthetic read, including explicit
  `absent: true` for NONE species/move/item/ability and no primary status.
- `UNAVAILABLE`: known unsupported sentinel, reserved item, DPE-only item
  exclusion, missing explicit BaseStats initializer, or field in an empty slot.
  Egg party stats/status/effective fields are withheld.
- `UNKNOWN`: missing/invalid/hole ID, inconsistent numeric field, unproved
  conditional ability selection, effective randomized types/moves/max PP, or
  malformed input. Nonverified fields have no value.

An unknown move invalidates its identity/baseline/PP without invalidating other
moves or independently checked HP. A missing/truncated/oversized block, bad
count or occupied-prefix mismatch returns six fresh entirely unknown rows.
There is no reuse of previous snapshots. PP bytes describe stored current PP;
effective maximum PP is unproved, so baseline PP is never used as a randomized
output cap. Unsupported status combinations/bits are withheld conservatively.

Conditional `GetMonAbility`/`TryRandomizeAbility`, contextual ability names,
effective randomized stats/move power/category/types and playable form support
remain unproved. No live reader, session acceptance, enemy/battle/T4 view or
Tracker UI/T5 is part of this module.

## Validation and handoff

Use the already available `/opt/homebrew/bin/lua5.4` (Lua 5.4.9); no installation
or tool-binary inspection is needed:

```sh
python3 07_scripts/tracker/run_cfru_dpe_party_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 -m unittest discover -s 07_scripts/tracker -p 'test_*.py' -v
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py --check
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check
```

| Check | Candidate result; rerun after final commit and bound in PR evidence |
| --- | --- |
| New Lua source/byte/confidence suite | PASS — 43 cases; every mapped catalog row, all supplemental numeric source fields, six slots, Gen1/mid-dex/Gen8/Gen9/regional controls and negative inputs |
| Existing #691 Lua source/mock lifecycle/SHA regressions | PASS — 55 cases, including eight SHA known-answer vectors |
| Python discovery: T1 + #691 + #692 isolation | PASS — 36 tests (33 existing + 3 new) |
| T1 profile `--check` | PASS — byte-identical |
| Git safety / whitespace / exact changed paths / Gitlinks | PASS; exact delivered commit recorded in PR |
| Lua 5.1 | NOT_RUN; no compatibility claim |
| Linux/BizHawk, actual output/session binding, live party/UI | NOT_RUN / PENDING_LINUX_HOST; production DENIED |

No ROM, save, build, emulator state, local manifest, `offsets.ini`, secret or tool
binary was inspected. The existing `CASUAL_NATDEX.rnqs` is untouched and excluded
from staging. No component source or Gitlink changes occur.

Next: review this bounded Phase A PR and accept its source/synthetic evidence.
Full T3 Phase B requires #689/#499 Linux-BizHawk PASS and #691 real output/session
activation acceptance first, then a separately authorized read-only live party
field-fidelity run. #692 stays open; no runtime compatibility is established.
