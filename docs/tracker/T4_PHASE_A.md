# T4 #693 — Mac-first source / synthetic battle decoder

**CONFIRMED SOURCE/SYNTHETIC EVIDENCE:** bounded Phase A candidate from Workspace
main `bacec6e5c6719063524aae8a164a73b9ca25e82c`, tree
`09f228846db7a19313a974ada1a1faa6ef3b7f8d`, on
`feature/693-source-battle-decoder-mock`. The
[updated #693 contract](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/693)
authorizes ROM-free preparation despite the unpassed live predecessors.

CONTROL review target: `CFRUDPE_TRACKER_BATTLE_DECODER_MOCK_READY`.
The marker requires CONTROL acceptance; these fixtures do not establish
`CFRUDPE_TRACKER_BATTLE_FIDELITY_READY`, complete T4 or close #693.

## Source identity and isolation

The detached [decoder](../../03_tools/tracker-extensions/CFRUDPEExtension/source_battle_decoder.lua)
loads only the accepted T3 source resolver and SHA helper. Production never
loads it. `CFRUDPEExtension.lua`, its #691 production-denied guard, the T3
decoder, T1 generator/profile and all component Gitlinks remain unchanged.

`newMock(publicJsonText, publicSourceTexts, publicMultiText)` uses T3's exact
whole-serialization lock: schema v2, JSON SHA-256
`8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981`, profile ID
`sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75`.
The same five pinned public source texts are required as in [T3](T3_PHASE_A.md).
The additional `CFRU:include/new/multi.h` is locked to its existing T1 input
hash `d6872f075e1be795b4253abe72d111f154a95ccb01e4e1900ee1544ad5060088`.
Only immutable, byte-exact accepted strings are cached. Profile objects and
decoder callbacks cannot substitute the accepted source facts.

Pins remain CFRU `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2`, DPE
`d887185de1f6ae6a78e85c4311bbadde17041d00`, UPR-FVX
`4670a5413104ec02bc08c09ff584470a8a6cb7bd`, Tracker
`c450ecaee2d8131a2789bb656e3be792a93712fb` and NatDexExtension
`a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.

The decoder's ABI constants are checked against the accepted T1 ARM record
layout, independently of the fixture's literal offsets:

| BattlePokemon surface | Offset / little-endian width |
| --- | --- |
| Row size | 88 (`0x58`), four rows |
| Species / moves | `0x00` u16 / `0x0C` four u16 |
| Ability / types 1, 2, 3 | `0x20`, `0x21`, `0x22`, `0x18` u8 |
| Current PP | `0x24` four u8 |
| HP / level / maxHP / item | `0x28` u16 / `0x2A` u8 / `0x2C` u16 / `0x2E` u16 |
| Primary / secondary status | `0x4C`, `0x50` u32 |

`include/battle.h` declares `gBattlerPartyIndexes` as four u16 entries,
`gBattlerPositions` as four u8 entries, `gBattlersCount` as u8 and
`gBattleTypeFlags` as u32. `include/constants/battle.h` defines the left
positions 0/1 and `BIT_SIDE=1`; `GET_BANK_SIDE` in `include/battle.h` uses
`GetBattlerPosition(bank) & BIT_SIDE`. Supporting pinned
`src/battle_util.c::GetBankPartyData` selects `gPlayerParty`/`gEnemyParty` using
that side and the battler's party index. No runtime addresses are used.

## Synthetic API and context contract

`transition(event)` immediately clears the current snapshot and advances the
epoch. `start` and `switch` arm a new synthetic context; `end`, `reset`,
`output-switch` and unrecognized events disarm it. `snapshot()` returns an
independent copy. Previously returned copies are historical samples; each
field carries `sampleEpoch`, and no old copy is the decoder's current state.

`decodeMock(sample)` takes strings and plain tables only:

- `epoch`: current decoder epoch.
- `before` / `after`: matching `epoch`, `state="ACTIVE"`, nonempty synthetic
  `output`/`battle` tokens, `flags` (4 bytes), `count` (1 byte), `positions`
  (4 bytes), `indexes` (8 bytes), and optional matching `trainerA` context.
- `battleMons`: exactly 352 synthetic bytes, distinct from 100-byte party rows.
- Optional `ppCaps`: 16 bytes of explicitly supplied, same-sample synthetic
  effective maximum PP, indexed by battler then move. This is a fixture trust
  declaration, not a runtime surface or proof of randomized move data.

Only normal non-link singles with flags `0x4` (wild) or `0xC` (trainer), count
two and left positions 0/1 are decoded. The source states IS_MASTER is set
in non-link battles; absent IS_MASTER is conservatively ambiguous.
Each active team index is read at `2 * battler`, checked in 0..5 and converted
to a separate 1..6 party slot. Inactive array entries are ignored. A team slot
never follows from the battler index alone.

Coherent four-battler flags `0x5`, `0xD`, `0x4F`, `0x20000D` and `0x40000D`
(double wild/trainer, link multi, two opponents, partner) are explicitly
`UNAVAILABLE`. Their slot/trainer ownership is deliberately not implemented.
Invalid counts, duplicate/illegal positions, illegal u16 indices and all other
unproved flag combinations are `UNKNOWN`, including special single modes.
High flag bits are read as u32 and never truncated into safe singles.

Missing/malformed blocks, stale epochs, before/after drift or an unannounced
change of output, battle, flags, positions, team index or trainer-A context
clear every current field and retire the epoch. A fresh coherent sample is
required. A switch must be declared before reading its new rows. These rules
are synthetic declarations: actual live lifecycle detection remains unproved.

## Fields, precedence and trainer limits

Every confidence-bearing field has `VERIFIED` / `UNAVAILABLE` / `UNKNOWN`,
`TEST_ONLY`, `liveConfidence=UNKNOWN`, provenance/reason and `sampleEpoch`.
Nonverified fields have no value. `VERIFIED` means source mapping or gated
synthetic bytes only. Numeric ranges never prove a loaded output or live layout.

Mapped active species, HP, level, moves, ability ID, held item and three types
come from the synthetic `gBattleMons` rows. Party data and source baselines
are separate and never serve as fallback. Unknown/unsupported/absent species
or a battle egg suppress dependent active fields. Bad HP invalidates the HP
pair; bad level invalidates level. Other mapping failures affect their fields
and dependents without replacing them with stock values.

PP needs a mapped move and an explicit valid synthetic effective cap; absent
moves require zero PP/cap. Missing caps, excessive PP or unknown moves yield
`UNKNOWN` PP. Baseline PP does not cap randomized output. Effective move
power/category/semantics remain `UNKNOWN`. Ability mapping is a baseline
catalog identity; `abilityName` remains separately `UNKNOWN` because dynamic
name selection is unproved. Form mappings do not certify form mechanics.

Primary status validates the source masks, toxic counter and locked FROSTBITE
configuration. Secondary status is an opaque u32 with the undeclared bit 7
rejected; its interpretation is `UNAVAILABLE`, including cross-battler and
counter semantics. This raw field does not certify a valid live status context.

Optional trainer A requires `{epoch, bytes=<u16 string>, trusted=<boolean>,
source="gTrainerBattleOpponent_A"}`. Only a trusted, matching trainer context
can publish that explicitly supplied synthetic ID. It does not resolve a real
`gTrainers` row/name/class or prove an enemy team. Missing/untrusted identity
is `UNKNOWN`; wild trainer identity is `UNAVAILABLE`. Trainer B is always
`UNAVAILABLE` in supported singles: pinned `include/new/multi.h` binds it to
`ExtensionState.trainerBTrainerId`, declared u16 in `include/battle.h`, with
no independently established absolute address. No trainer table is decoded.

## Verification and handoff

Use the already available `/opt/homebrew/bin/lua5.4`; no tool installation or
binary inspection is required:

```sh
python3 07_scripts/tracker/run_cfru_dpe_battle_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/tracker/run_cfru_dpe_party_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 -m unittest discover -s 07_scripts/tracker -p 'test_*.py' -v
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py --check
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check
```

| Check | Candidate result; exact post-commit run bound in PR evidence |
| --- | --- |
| T4 Lua 5.4 synthetic battle suite | PASS — 76 cases |
| T3 Lua source/party suite | PASS — 43 cases |
| T2 Lua mock lifecycle/SHA suite | PASS — 55 cases |
| Full T1/T2/T3/T4 Python discovery | PASS — 40 tests |
| T1 `--check` | PASS — byte-identical public profile |
| Git safety, whitespace, exact paths and Gitlinks | PASS; final revision in PR |
| Lua 5.1 | NOT_RUN; compatibility unclaimed |
| Actual BizHawk/Tracker battle runtime, live trainer/output/UI | NOT_RUN; production activation DENIED |

No protected/private artifact, ROM, save, state, build, local manifest,
`offsets.ini`, emulator memory or tool binary was inspected. Known untracked
`CASUAL_NATDEX.rnqs` remains untouched and unstaged. There is no T5 UI work,
Tracker-core change, engine change, Gitlink change or live runtime claim.

Next: CONTROL reviews the bounded PR and its exact revision-bound Phase A
evidence for acceptance of `CFRUDPE_TRACKER_BATTLE_DECODER_MOCK_READY`.
#693 remains open for separately authorized Phase B after the live predecessors.
