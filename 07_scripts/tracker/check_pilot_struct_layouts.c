/* Source-only design assertions; compile with ARM GCC -fsyntax-only, never link.
 * -I must point to an isolated exact CFRU source revision. No memory/ROM input. */
#include <stddef.h>
#include "include/global.h"
#include "include/pokemon.h"
#include "include/battle.h"
#include "include/item.h"
#include "include/global.fieldmap.h"

#define SIZE(type, size) _Static_assert(sizeof(struct type) == (size), #type " size")
#define OFFSET(type, field, offset) _Static_assert(offsetof(struct type, field) == (offset), #type "." #field)

SIZE(Pokemon, 0x64);
SIZE(BoxPokemon, 0x50);
OFFSET(Pokemon, backupSpecies, 0x1C);
OFFSET(Pokemon, teraType, 0x1E);
OFFSET(Pokemon, species, 0x20);
OFFSET(Pokemon, item, 0x22);
OFFSET(Pokemon, experience, 0x24);
OFFSET(Pokemon, moves, 0x2C);
OFFSET(Pokemon, pp, 0x34);
OFFSET(Pokemon, hpEv, 0x38);
OFFSET(Pokemon, condition, 0x50);
OFFSET(Pokemon, level, 0x54);
OFFSET(Pokemon, hp, 0x56);
OFFSET(Pokemon, maxHP, 0x58);
SIZE(BaseStats, 0x1C);
OFFSET(BaseStats, ability1, 0x16);
OFFSET(BaseStats, ability2, 0x17);
OFFSET(BaseStats, hiddenAbility, 0x1A);
SIZE(BattlePokemon, 0x58);
OFFSET(BattlePokemon, type3, 0x18);
OFFSET(BattlePokemon, statStages, 0x19);
OFFSET(BattlePokemon, ability, 0x20);
OFFSET(BattlePokemon, type1, 0x21);
OFFSET(BattlePokemon, item, 0x2E);
OFFSET(BattlePokemon, status1, 0x4C);
SIZE(BattleMove, 12);
OFFSET(BattleMove, split, 10);
SIZE(Trainer, 0x28);
OFFSET(Trainer, party, 0x24);
SIZE(TrainerMonNoItemDefaultMoves, 8);
SIZE(TrainerMonItemDefaultMoves, 8);
SIZE(TrainerMonNoItemCustomMoves, 16);
SIZE(TrainerMonItemCustomMoves, 32);
OFFSET(TrainerMonItemCustomMoves, ability, 6);
OFFSET(TrainerMonItemCustomMoves, nature, 7);
OFFSET(TrainerMonItemCustomMoves, ivSpread, 8);
OFFSET(TrainerMonItemCustomMoves, evSpread, 14);
OFFSET(TrainerMonItemCustomMoves, heldItem, 20);
OFFSET(TrainerMonItemCustomMoves, moves, 22);
OFFSET(TrainerMonItemCustomMoves, teraType, 30);
SIZE(LevelUpMove, 3);
OFFSET(LevelUpMove, level, 2);
SIZE(Item, 0x2C);
OFFSET(Item, pocket, 0x1A);
SIZE(MapHeader, 0x1C);
OFFSET(MapHeader, mapLayoutId, 0x12);
