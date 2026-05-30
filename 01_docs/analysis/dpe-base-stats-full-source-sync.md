# DPE Base Stats full source sync audit

Date: 2026-05-30
Branch: `analysis/dpe-base-stats-full-source-sync`
Scope: read-only source audit. No DPE/CFRU/UPR-FVX table, submodule pin, external source, ROM, save, build artifact, tool binary, screenshot, raw report, hash, private path, token, secret, or `.env` data was changed.

## Question

Can local DPE `src/Base_Stats.c` be safely replaced fully or mostly from a current compatible Gen9 DPE/CFRU source?

Short answer: no. A full replace is not recommended.

The only complete source with matching local IDs, struct fields, and constants is the current Planton DPE fork line itself. Its final `origin/master` merge commit `34f88ab9fb2d23db715297016f00d1c5e30b064d` has no tree diff against the local checked DPE data commit `1c8d53870e38d7019c681a68a17c9425a3490611` for the audited files. That is a valid pin/source confirmation, not a useful replacement source.

## Local DPE shape

Audited local paths:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/base_stats.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/abilities.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/types.h`

Local table shape:

- `struct BaseStats` fields are the CFRU/DPE-style split fields: base stats, two types, catch/EXP, bitfield EV yields, held items, gender, egg cycles, friendship, growth, egg groups, `ability1`, `ability2`, `hiddenAbility`, safari flee, body color, and `noFlip`.
- `ability_t` is `u8`; Ability assignments depend on local `ABILITY_*` IDs and alias defines.
- `NUM_SPECIES` is `(SPECIES_PECHARUNT + 1)`, with `SPECIES_PECHARUNT = 0x59F`.
- Local `gBaseStats[]` has explicit rows through `SPECIES_PECHARUNT`.
- Local Ability header contains Gen9-looking aliases such as `ABILITY_HADRONENGINE ABILITY_ELECTRICSURGE`, `ABILITY_ORICHALCUMPULSE ABILITY_DROUGHT`, `ABILITY_GOODASGOLD ABILITY_CLEARBODY`, and `ABILITY_ZEROTOHERO ABILITY_TORRENT`.

## Source checks

| Source | Base Stats shape | Species/order compatibility | Ability-ID compatibility | Form coverage | Drop-in result |
| --- | --- | --- | --- | --- | --- |
| Planton DPE `origin/master` `34f88ab9fb2d23db715297016f00d1c5e30b064d` | Same files/struct; no audited-file tree diff vs local data commit | Same `NUM_SPECIES`, same `SPECIES_PECHARUNT` end, same local form IDs | Same aliases and risks | Same as local | Compatible but not useful as replacement; it is the accepted local line. |
| Shiny-Miner DPE Gen9 `master` `5906aa4d4904e41393fd9184a16951c961e96263` | Same `struct BaseStats` field shape and headers | Header order matches local through Pecharunt | Header aliases match local risk shape | Missing four explicit Ogerpon Terastal `Base_Stats.c` rows now present locally; full replace would revert accepted local fixes | Not recommended for full replace. Potentially useful as format baseline only. |
| Skeli789 DPE `master` `cdfc053a56326a13dc5311b24488445e17536b7e` | Same broad struct shape, but older constants | Ends at `SPECIES_URSHIFU_RAPID_GIGA`; no Pecharunt / Terapagos / Ogerpon Gen9 tail | No local Gen9 alias layer | Missing Gen9 tail and local form IDs | Not compatible for Gen9 full replace. |
| pokeemerald-expansion | Modern GBA data, but `SpeciesInfo` shape with `.types`, `.abilities[]`, learnsets and graphics/data in a combined species-info model | Different constants/order/model | Different ability constants and config-driven behavior | Useful reference for Gen9 data semantics, not DPE table shape | Not a drop-in source. |
| Pokemon Showdown `data/pokedex.ts` | TypeScript object data, not C `struct BaseStats` | Name/form mapping required; no local IDs | Ability names, not local effect IDs | Current canonical-ish data, but form names and support policy need alias table | Reference input only; not a drop-in source. |

Primary web/source references checked read-only:

- Shiny-Miner DPE Gen9: <https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9>
- Skeli789 Dynamic Pokemon Expansion: <https://github.com/Skeli789/Dynamic-Pokemon-Expansion>
- pokeemerald-expansion Pokemon data: <https://github.com/rh-hideout/pokeemerald-expansion/tree/master/src/data/pokemon>
- Pokemon Showdown data: <https://github.com/smogon/pokemon-showdown/tree/master/data>

## Key findings

- Local DPE and Planton DPE `origin/master` are compatible and effectively identical for the audited files. No replacement is needed there.
- Shiny-Miner/DPE Gen9 is the closest external format sibling, but it is behind the local accepted table state. A full replace from it would remove the accepted Ogerpon Terastal `Base_Stats.c` rows and undo the tranche-1 fields.
- Skeli789/DPE is the upstream format ancestor but not a Gen9 source. Its species set ends before the local Gen9 tail and cannot cover Pecharunt, Terapagos, Ogerpon Terastal, or other local Gen9 additions.
- pokeemerald-expansion is useful for GBA-shaped data sanity checks, but its species data model is not the DPE `Base_Stats.c` layout.
- Pokemon Showdown remains the best machine-readable current Pokemon-data reference, but it requires mapping and field conversion; it does not include all DPE fields used by the prior dry-diff path.

## Form and alias risks

- Ogerpon: local IDs include base masks and four Terastal rows. Shiny-Miner headers match the names, but its fetched `Base_Stats.c` lacks the four local accepted Terastal rows.
- Terapagos: local IDs include base, Terastal, and Stellar forms, but Ability behavior remains risky because Tera-related Ability support is not a plain DPE data question.
- Alcremie: local constants are sweet-name forms such as `SPECIES_ALCREMIE_STRAWBERRY`, `SPECIES_ALCREMIE_BERRY`, and related variants, not a single `SPECIES_ALCREMIE` mapping.
- Basculin/Basculegion: local constants use explicit local form names such as `SPECIES_BASCULEGION_M` and `SPECIES_BASCULEGION_F`, not a generic Showdown-style key.
- Pumpkaboo/Gourgeist: local constants include both base and size-specific shortforms. Size semantics remain a mapping risk.
- Sinistea/Polteageist: local constants include base and `CHIPPED` forms. Antique/authentic naming remains a mapping risk.
- Ability aliases: many Gen9 names compile to older local IDs. Even if a source has a matching Ability name, it is not proof of matching battle behavior.

## Recommendation

Do not do a full `Base_Stats.c` replace.

Use a staged update path instead:

1. Keep Planton DPE `origin/master` as the local compatible source of truth.
2. Continue using the reviewed Showdown-to-local alias table and the dry-diff helper for non-Ability fields.
3. Split future DPE data PRs by field family:
   - Types / egg groups / gender first.
   - Raw base stat corrections only after deciding whether local balance buffs should be preserved.
   - Catch Rate, EXP Yield, EV Yield, and Growth Rate only after a secondary trusted source is selected.
   - Ability assignments only after Ability behavior blockers are accepted, fixed, or explicitly excluded.
4. Treat Shiny-Miner DPE as a format and history reference, not as an overwrite source.
5. Treat pokeemerald-expansion and Pokemon Showdown as converter inputs/sanity references, not as C table drop-ins.

## Later data PR handoff

The next real DPE data PR should not start from a whole-file replacement. It should start from a generated review table with:

- Species key.
- Local DPE ID.
- Source key.
- Field-by-field proposed changes.
- Ability blocker status.
- Form/open-risk blocker status.
- Whether the change is a canonical correction or likely local balance policy.

Only rows classified as non-blocking and explicitly reviewed should be written to DPE.
