# Pokemon Data Alias Map Policy

Date: 2026-05-29

Branch: `analysis/pokemon-data-alias-map`

Scope: policy and sanitized summary only. No CFRU, DPE, UPR-FVX, submodule pin, Pokemon Showdown source file, raw audit report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data is changed or committed.

## Inputs

- PR #422: Pokemon Showdown mapping audit plan and read-only helper.
- Local full audit against an external Pokemon Showdown `data/` directory.
- Local CFRU/DPE constants for Species, Moves and Abilities.

The full audit output is intentionally not committed. This document preserves only categorized counts, examples and review policy.

## Full-Audit Summary

| Area | Audit summary | Policy result |
| --- | --- | --- |
| Species | Local CFRU and DPE each expose 1415 Species constants. Showdown had 319 normalized species keys without a local constant; local constants had 221 normalized keys without a Showdown key. | Mostly expected form/mod/local naming drift. Requires alias map before generated data updates. |
| Moves | Local CFRU and DPE each expose 993 Move constants. Showdown had 104 normalized move keys without a local constant; local constants had 143 normalized keys without a Showdown key. | Mostly Z/Max/GMax split constants and Hidden Power variants. A small real-risk set remains. |
| Abilities | CFRU exposes 289 Ability constants and DPE exposes 288. Showdown had 36 normalized ability keys without a local constant; local constants had 8 normalized keys without a Showdown key. | Highest-risk area because local aliases can preserve names while using older behavior. |
| Ability aliases | The local audit reported 67 alias define rows across CFRU/DPE ability headers. | Treat as behavior-risk findings, not solved mappings. |

## Species Policy

| Category | Examples | Policy |
| --- | --- | --- |
| True form-name aliases | Ogerpon Terastal forms: Showdown `ogerpontealtera`, `ogerponwellspringtera`, `ogerponhearthflametera`, `ogerponcornerstonetera`; CFRU `OGERPON_GREEN/BLUE/RED/GREY`; DPE `OGERPON_*_TERASTAL`. | Map explicitly by intended form and local numeric ID. Do not infer from normalized names alone. |
| Local short forms | `arcanineh`, `articunog`, `farfetchdg`, `taurosp`, `taurosblazep`, `taurosaquap`, `urshifurapid`, `indeedeefemale`, `meowsticfemale`. | Allow through a reviewed alias table. Prefer long Showdown-style names as canonical keys and local constants as targets. |
| GMax/Giga name aliases | Showdown `charizardgmax`, `blastoisegmax`, `rillaboomgmax`; local `charizardgiga`, `blastoisegiga`, `rillaboomgiga`. | Alias `gmax` to local `giga` only for known Gigantamax forms. Do not apply broad string replacement outside this category. |
| Cosmetic/form naming aliases | Unown letters, Flabebe/Floette/Florges colors, Furfrou trims, Sawsbuck seasons, Minior forms, Pumpkaboo/Gourgeist sizes, Pikachu cap names. | Alias or ignore depending on whether the local table has distinct gameplay data. Cosmetic-only forms can be ignored for Base Stats but may need explicit handling for species pools. |
| CAP/Fanmons / consciously ignore | Showdown keys such as `ababo`, `argalis`, `arghonaut`, `astrolotl`, `aurumoth`, `brattler`, `cawmodore`, `colossoil`, `krilowatt`, `miasmaw`, `pajantom`, `plasmanta`, `saharaja`. | Ignore for CFRU/DPE Gen9 baseline unless the project explicitly adopts CAP/fan content later. |
| Local extras | `none`, `egg`, `shadowwarrior`, local-only helper/species placeholders, and local special forms that have no Showdown equivalent. | Ignore for Showdown data import. Keep documented so generated audits do not repeatedly flag them as missing Showdown data. |
| Genuine open risks | Alcremie cream/sweet encoding, Sinistea/Polteageist antique/chipped naming, Basculegion gender/form naming, Indeedee/Meowstic gender naming, Ogerpon mask-vs-Terastal names. | Require manual review before generated updates. These can affect Base Stats, learnsets, abilities or compatibility by form. |

## Move Policy

| Category | Examples | Policy |
| --- | --- | --- |
| Z-Move physical/special local split | Showdown `breakneckblitz`, `alloutpummeling`, `blackholeeclipse`; local `*_P` and `*_S`. | Map one Showdown key to two local constants only for move-behavior/table coverage. Do not use split constants as normal learnset targets. |
| Max/GMax physical/special local split | Showdown `maxstrike`, `maxairstream`, `gmaxvinelash`, `gmaxwildfire`; local `MAX_*_P/S`, `G_MAX_*_P/S`. | Same split policy as Z-Moves. Treat these as engine/generated battle moves, not ordinary Pokemon learnset moves. |
| Hidden Power type variants | Showdown `hiddenpowerbug`, `hiddenpowerdark`, `hiddenpowerfire`, etc. | Ignore as Showdown-side typed variants unless a future engine branch models each variant as a distinct local move. |
| Spelling aliases | Showdown `visegrip`; local `vicegrip`. | Allow narrowly in alias map. Do not generalize spelling rewrites. |
| Consciously ignore | CAP/fan moves such as `paleowave` and `shadowstrike`; partner-only or mode-specific moves if the project does not support that mode. | Ignore for baseline CFRU/DPE Gen9 Pokemon data unless a later scope explicitly adopts that mode/content. |
| Local extras | `none`, `namelength`, `leechfang`, `steelyhit`, engine helper moves or project-local moves. | Keep local-only. Never map Showdown data onto helper constants without a code-backed reason. |
| Genuine open risks | Showdown `allyswitch`; Let's Go partner moves such as `baddybad`, `bouncybubble`, `buzzybuzz`, `floatyfall`, `sappyseed`, `zippyzap`; any current-game move not explained by split/variant/ignore policy. | Review against CFRU move behavior before data import. Missing real move constants may require engine work, not just table data. |

## Ability Policy

| Category | Examples | Policy |
| --- | --- | --- |
| Real local aliases to older effects | `HADRONENGINE -> ELECTRICSURGE`, `ORICHALCUMPULSE -> DROUGHT`, `POISONPUPPETEER -> PLUS`, `GOODASGOLD -> CLEARBODY`, `BEADSOFRUIN/SWORDOFRUIN/TABLETOFRUIN/VESSELOFRUIN -> STALL`, `SUPREMEOVERLORD -> HUGEPOWER`. | Mark as unresolved behavior risk. Name match is not enough to claim Gen9 correctness. |
| Name mismatch | Showdown `tabletsofruin` vs local `tabletofruin`; Showdown `asoneglastrier/asonespectrier` vs local `asonegrim/asonechilling`; Showdown `noability` vs local `none`; CFRU `LINGERINGAROMA` vs DPE `UNUSED` on `0x4D`. | Use explicit alias entries only after confirming the intended local constant and behavior. |
| Probably missing true Gen9 behavior | `commander`, `hospitality`, `embodyaspect*`, `teraformzero`, `terashell`, `terashift`, plus aliased Gen9 abilities such as `goodasgold`, `toxicdebris`, `zerotohero`, `myceliummight`. | Do not resolve by naming alone. Needs a CFRU ability-behavior audit or implementation branch. |
| Consciously ignore | CAP/fan abilities such as `mountaineer`, `persistent`, `rebound`, `megasol`, `spicyspray`; merged legacy equivalents where CFRU intentionally uses one effect for both names, such as `airlock/cloudnine`, `purepower/hugepower`, `libero/protean`, `wimpout/emergencyexit`. | Ignore or document as intentional merged behavior. Do not create new IDs without gameplay policy approval. |
| Local-only abilities | `portalpower`, `evaporate`, `drillbeak`, `unused`, `none`. | Keep local-only unless a later source-backed task proves a Showdown equivalent or removes the local placeholder. |

## Alias-Map Rules

1. The alias map is a review artifact, not permission to change CFRU/DPE data.
2. Every alias entry needs a category: `form-name`, `local-shortform`, `gmax-giga`, `split-move`, `hidden-power-variant`, `spelling`, `local-extra`, `fan-ignore`, or `behavior-risk`.
3. Species aliases may map by normalized name only after form family, form meaning and local numeric ID are reviewed.
4. Move aliases may map one Showdown move to multiple local constants only for documented split families such as Z-Move and Max/GMax physical/special pairs.
5. Ability aliases that point to older effects must stay `behavior-risk` until CFRU behavior is audited. They must not be counted as solved Gen9 behavior.
6. Ignore entries should be explicit and reasoned, especially CAP/fan content, Pokestar/Totem-only forms, helper constants, and project-local placeholders.
7. Generated data updates must fail closed on uncategorized unresolved mappings.

## Handoff Prompt

Continue from `analysis/pokemon-data-alias-map`. Build a small reviewed alias table from this policy without editing CFRU/DPE data tables. Start with Ogerpon forms, regional/local short forms, GMax/Giga species aliases, Z/Max/GMax split move aliases, Hidden Power variants, and Ability behavior-risk aliases. Any uncategorized Species/Move/Ability key should block generated data updates until reviewed.
