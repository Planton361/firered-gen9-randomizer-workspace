# National Dex Handoff Safety — CFRU/DPE and UPR-FVX

Workspace Issue [#545](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/545)

**Evidence class:** source/static analysis only

**Scope:** National Dex ownership and compatibility at the post-Parcel Pokédex handoff

## Revision basis

| Source | Exact revision |
|---|---|
| Workspace | [73d12b26cd0ed28c4bf1a0c5b2fb55980c1fcfbf](https://github.com/Planton361/firered-gen9-randomizer-workspace/tree/73d12b26cd0ed28c4bf1a0c5b2fb55980c1fcfbf) |
| CFRU | [ec4e1b7410a65b23e081010c580ecb8c078a64a1](https://github.com/Planton361/CFRU-expansion/tree/ec4e1b7410a65b23e081010c580ecb8c078a64a1) |
| DPE | [22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/tree/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc) |
| UPR-FVX | [0e3be63e94e34215cc35308d64e8db15e9a3c48c](https://github.com/Planton361/universal-pokemon-randomizer-fvx/tree/0e3be63e94e34215cc35308d64e8db15e9a3c48c) |
| NatDex FireRed reference | [CyanSMP64/pokefirered b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7](https://github.com/CyanSMP64/pokefirered/tree/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7) |
| pret FireRed source baseline | [e060ab955b5dc9ac1c4904c2cd141683615cf477](https://github.com/pret/pokefirered/tree/e060ab955b5dc9ac1c4904c2cd141683615cf477) |

The Workspace HEAD and CFRU, DPE, and UPR-FVX Gitlinks match Issue #545. The NatDex commit was inspected directly from its exact commit object; the pret link is the Workspace's checked-out source reference. Only tracked source, assembly, scripts, headers, and configuration were inspected. No ROM, save, build, emulator state, release binary, private path, or secret was accessed. No build or runtime test was performed.

## Findings

### CFRU and DPE do not currently enable National Dex

At the pinned CFRU revision, **FLAG_SYS_NATIONAL_DEX** is defined but has no source or assembly setter/use. **VAR_NATIONAL_DEX** is not defined or referenced; CFRU has only the unused generic alias **VAR_0x404E**. Its **EnableNationalPokedex** occurrence is a header declaration, not an implementation or call. The **nationalMagic** field occurs only in the CFRU copied structure declaration. Searches for BPRE's National Dex stored value **0x6258** and flag value **0x0840** found no CFRU code/script writes. The CFRU linker maps only the getter **IsNationalPokedexEnabled** to the BPRE routine at **0x0806E25C | 1**; this is a Thumb-tagged read binding, not an activation binding. See [CFRU flags](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/include/constants/flags.h#L1372), [variables](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/include/constants/vars.h#L121-L123), [event declarations](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/include/event_data.h#L20-L24), [structure](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/include/global.h#L293-L302), and [linker binding](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/BPRE.ld#L2439).

The CFRU structure comment is not the BPRE enable contract: it labels **Pokedex + 0x02** as **nationalMagic** and says **0xDA**, while BPRE defines its National marker at **Pokedex + 0x03** as **0xB9**. No CFRU code reads or writes the copied field. Its **VAR_0x404E** alias also has no call site. This copied layout/comment must not be used to implement BPRE activation.

The current M-007 Parcel handoff sets **FLAG_SYS_POKEDEX_GET**, calls **SetUnlockedPokedexFlags**, then awards five Poké Balls. Its comments explicitly defer National Dex. The insertion script asserts that **EnableNationalPokedex** is absent. Vanilla **SetUnlockedPokedexFlags** changes three GCN link bits; it does not set the National Dex marker, variable, or flag. Thus neither the Pokedex-get flag nor this unlock special activates National Dex. See the [M-007 handoff](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/assembly/overworld_scripts/shortened_oak_parcel_flow.s#L95-L105), [insertion assertions](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/scripts/insert.py#L1395-L1416), and [pret implementation of SetUnlockedPokedexFlags](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/src/save_location.c#L98-L103).

At the pinned DPE revision, there is no National Dex flag/variable/magic write or repair path. DPE maps the same BPRE getter and consumes it in two relevant places: the assembly display-number hook selects National versus regional numbering, and **DexScreen_InitGfxForTopMenu** selects the National mode/count display when the getter is true. The expanded Pokédex allocation hook reserves larger data independently; allocation is not activation. Calls to **GetSetPokedexFlag** record/read per-species seen/caught state and do not toggle the global National mode. See [DPE linker bindings](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/BPRE.ld#L15-L21), [Pokédex hooks](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/assembly/pokedex_hooks.s#L4-L51), and [DPE mode selection](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/updated_code.c#L620-L655). CFRU's own direct consumer is an evolution guard that calls the BPRE getter; it does not set state ([source](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/src/mid_battle_evo.c#L267-L278)).

**Result:** no current CFRU or DPE new-game, load, save, Parcel, or options path enables or repairs any of the three BPRE National Dex fields. DPE's expanded display consumes the global mode state; it does not establish it.

### Complete BPRE operation and callable binding

BPRE stores three independent pieces of National Dex state:

| State | BPRE meaning |
|---|---|
| **gSaveBlock2Ptr->pokedex.nationalMagic** | byte at **Pokedex + 0x03**, set to **0xB9** |
| **VAR_NATIONAL_DEX** | variable ID **0x404E**; its stored value must be **0x6258** |
| **FLAG_SYS_NATIONAL_DEX** | system flag at **SYS_FLAGS + 0x40**, set |

The value **0x6258** is the value written to variable **0x404E**; it is not the variable's ID. **IsNationalPokedexEnabled** returns true only when all three match, so a flag-only or variable-only approximation is incomplete. **EnableNationalPokedex(void)** writes all three; the paired disable routine clears all three. These semantics are present in both the Workspace's pret source and exact NatDex source: [pret implementation](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/src/event_data.c#L91-L115), [NatDex implementation at Issue pin](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/src/event_data.c#L83-L107), [NatDex variable ID](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/include/constants/vars.h#L128), [flag ID](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/include/constants/flags.h#L1398), and [save metadata layout](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/include/global.h#L183-L199).

There is no proved direct CFRU setter address in **BPRE.ld**; only **IsNationalPokedexEnabled** is mapped. Do not derive an **EnableNationalPokedex** address from that getter. The exact safe binding is the existing BPRE script special: **EnableNationalPokedex** is entry **0x016F** in the ordered **def_special** table at both the pret and NatDex pins. It is a no-argument, void special. A script **special 0x016F** dispatches through the original BPRE special table, so no hand-written C call, Thumb-address guess, or register-clobber assumption is needed. The current CFRU M-007 overlay already invokes BPRE special **0x0181** (**SetUnlockedPokedexFlags**) through the same dispatcher; the ordered table confirms that binding. See [pret BPRE special table](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/specials.inc#L378-L396), [NatDex BPRE special table](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/data/specials.inc#L378-L396), and [CFRU M-007 special binding](https://github.com/Planton361/CFRU-expansion/blob/ec4e1b7410a65b23e081010c580ecb8c078a64a1/assembly/overworld_scripts/shortened_oak_parcel_flow.s#L8-L23). Vanilla's later Oak's Lab Pokédex-upgrade script itself calls **special EnableNationalPokedex** ([pret map script](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PalletTown_ProfessorOaksLab/scripts.inc#L101-L109)).

Plain script operations that set the variable and flag cannot reproduce the full operation because they do not write **SaveBlock2.pokedex.nationalMagic**. A new source helper could do so, but the existing BPRE special is the smaller exact operation. It updates existing save metadata, one existing story variable, and one existing system flag; it adds no field or save-size change. The CFRU header's different **0xDA** comment is why the future implementation should invoke the BPRE special rather than directly write through that copied structure.

The NatDex reference's fresh-New-Game call is a separate RSE operation: **EnableNationalPokedex_RSE** writes **0xDA**, value **0x0302**, and **FLAG_0x838**. The same reference labels those as RSE values; they are not the BPRE triple above and do not establish the requested handoff timing ([reference new-game call](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/src/new_game.c#L125-L135), [RSE and BPRE routines](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/src/event_data.c#L61-L107)).

### UPR-FVX Misc option and generic FRLG mutations

**NATIONAL_DEX_AT_START** remains a Misc tweak (**1 << 7**). The UPR-FVX BPRE 1.0 entry sets **NationalDexTweakPossible=1**; **miscTweaksAvailable()** exposes the option from that value without checking the CFRU/DPE profile flag, and **applyMiscTweak()** always dispatches it to generic **patchForNationalDex()**. The handler separately detects CFRU/DPE Gen9 BPRE profiles, but that detection does not guard this option. See [tweak definition](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/0e3be63e94e34215cc35308d64e8db15e9a3c48c/romio/src/main/java/com/uprfvx/romio/MiscTweak.java#L49), [BPRE 1.0 profile](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/0e3be63e94e34215e9a3c48c/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini#L550-L635), [CFRU/DPE profile detection](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/0e3be63e94e34215e9a3c48c/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java#L666-L703), and [option availability/dispatch](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/0e3be63e94e34215e9a3c48c/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java#L8392-L8438).

For FRLG, **patchForNationalDex()** assumes the original byte signatures and free space are usable. It allocates ten bytes, rewrites the located script entry to point at the new routine, and writes the routine containing **setflag 0x0829**, **special 0x0181**, **special 0x016F**, then **end**. It also changes four other vanilla FRLG check families:

| Family | Generic FRLG operation |
|---|---|
| Pokédex-get script signature **292908258101** | Require one unique match, replace its first six bytes with a pointer-call/end, and install the ten-byte routine above |
| National Dex flag checkers | Find all **frlgNatDexFlagChecker** matches and replace them with **frlgE4FlagChecker** (the source comment describes the replacement as the Elite Four/Gary flag) |
| Oak's Lab Kanto-Dex checker | If a unique **frlgOaksLabKantoDexChecker** match is found, replace it with **frlgOaksLabFix** |
| Oak outside the house | If a unique **frlgOakOutsideHouseCheck** match is found, replace it with **frlgOakOutsideHouseFix** |
| Oak Aide check | If a unique **frlgOakAideCheckPrefix** match is found, change its conditional branch byte to **0xE0**, forcing the National Dex seen/caught branch |

The exact signatures and replacements are in [Gen3Constants](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/0e3be63e94e34215cc35308d64e8db15e9a3c48c/romio/src/main/java/com/uprfvx/romio/constants/Gen3Constants.java#L157-L175); the writes and allocation are in [patchForNationalDex](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/0e3be63e94e34215cc35308d64e8db15e9a3c48c/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java#L6886-L6989). UPR-FVX's [find helper](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/0e3be63e94e34215cc35308d64e8db15e9a3c48c/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java#L6769-L6798) rejects both missing and non-unique signatures.

The M-007 Parcel script emits the same **setflag FLAG_SYS_POKEDEX_GET** / **special 0x0181** sequence identified by UPR-FVX's six-byte script signature. The generic finder requires that signature to be unique and the patch aborts when it is missing or duplicated. If the CFRU-owned sequence is the unique match, UPR rewrites it and adds National activation; if other copies remain, the uniqueness check fails. No CFRU/DPE-specific disambiguation exists. Because the patch also rewrites the Oak/Aide/E4 check families, it is structurally unsafe for this profile. Today it is not redundant with CFRU/DPE, since those sources do not activate National Dex. If the ROM handoff owns activation and the option remains enabled, the option becomes a second script-rewrite/activation path.

This source overlap proves a compatibility hazard, not a specific runtime failure. The generic code's actual match selection against a generated ROM was not inspected.

## Ownership decision and follow-up boundaries

**Safest model: ROM-owned National Dex timing; UPR-FVX suppresses the legacy Misc option for the detected CFRU/DPE BPRE profile.** Put the full BPRE operation at the source-owned M-007 Parcel Pokédex handoff, using the exact BPRE **EnableNationalPokedex** special binding (**0x016F**). Keep National Dex disabled during Fresh New Game. UPR-FVX should continue to expose its existing behavior for vanilla FRLG.

Separate follow-up scopes:

1. **CFRU implementation issue:** add the BPRE special call at the M-007 Pokédex handoff after Parcel, without calling a guessed address or writing only a flag/variable. Check source ordering and preserve the existing item/story flow.
2. **UPR-FVX guard issue:** hide/mark **NATIONAL_DEX_AT_START** unavailable for the detected CFRU/DPE Gen9 BPRE profile and guard its apply path against stale/serialized settings. Preserve the vanilla FRLG option and implementation.
3. **Revision-bound verification before runtime:** static checks that the CFRU handoff calls special **0x016F** only at the intended event and that the BPRE special table maps it to **EnableNationalPokedex**; profile tests that the UPR option is unavailable and cannot apply for CFRU/DPE but remains available for vanilla FRLG; then targeted runtime checks that all three BPRE fields remain false before the handoff, become true at it, survive save/reload, and enable DPE National view/numbering. Verify vanilla FRLG behavior separately.

The user's historical crash report is **UNKNOWN as to root cause**. No sanitized failing fixture or allowed runtime reproduction was available. This audit makes no crash-causation claim.

## Verification record

- Source-only inspection at the exact revisions above; no ROM or private artifact access.
- No component source, Gitlink, build, test, or runtime changes.
- Workspace safety check passed before and after the report change.
- **git diff --cached --check** passed; the staged diff contains only this report.
- No component source, Gitlink, build, test, or runtime changes.

NATIONAL_DEX_HANDOFF_SAFE_WITH_ROM_OWNERSHIP
