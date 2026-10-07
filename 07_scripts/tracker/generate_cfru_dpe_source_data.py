#!/usr/bin/env python3
"""Locked, public-source-only CFRU/DPE profile. No game/build inputs.

The parsers deliberately accept only the locked source dialect. Unsupported or
ambiguous syntax fails; changing the lock requires review, not a best effort.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

SCHEMA = "cfru-dpe-tracker-source-profile"
VERSION = 2
PRODUCT = "3bdfe9919afc0b7bea55c79f37285e832be495c3"
PRODUCT_TREE = "f6bc65355811d7de153a91091b223fec9b50991e"
CONTRACT = "e6e0e867a5cca4fd2d373acf82504af45986e6fa"
CONTRACT_TREE = "d3b5b87fd8575ef4313e32be9c3e9490c3fe9b11"
PINS = {
    "CFRU": ("02_external/CFRU-expansion", "e68a701aa4e68733ef8ad1e7cadb68825c0d16c2"),
    "DPE": ("02_external/Dynamic-Pokemon-Expansion-Gen-9", "d887185de1f6ae6a78e85c4311bbadde17041d00"),
    "UPR-FVX": ("02_external/upr-fvx", "4670a5413104ec02bc08c09ff584470a8a6cb7bd"),
    "Tracker": ("02_external/Ironmon-Tracker", "c450ecaee2d8131a2789bb656e3be792a93712fb"),
    "NatDex-reference": ("02_external/NatDexExtension", "a94b8844800308248bb5090b6c36c8b2d7e5d7b9"),
}
GENERATOR = "07_scripts/tracker/generate_cfru_dpe_source_data.py"
OUTPUT = "03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json"
EXTENSION = "03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua"
EXTENSION_BLOB = "294cac84152e87010eb806c6331c90100d204a83"
# Only these public text objects may enter the generator; never scan a worktree.
INPUTS = {
    "CFRU": [
        "include/constants/species.h", "include/constants/moves.h",
        "include/constants/abilities.h", "include/constants/items.h",
        "strings/attack_name_table.string", "strings/ability_name_table.string",
        "strings/type_names.string", "charmap.tbl", "include/easy_text.h",
        "include/pokemon.h", "include/battle.h", "include/global.h", "include/item.h",
        "include/constants/battle.h",
        "include/gba/types.h", "src/config.h", "src/defines.h",
        "src/Tables/item_tables.c", "src/Tables/battle_moves.c",
        "src/ability_util.c", "src/build_pokemon.c", "src/util.c",
        "include/new/rom_locs.h", "include/new/multi.h", "BPRE.ld", "repointall",
        "scripts/string.py",
    ],
    "DPE": [
        "include/species.h", "include/moves.h", "include/abilities.h",
        "include/items.h", "include/base_stats.h", "src/defines.h",
        "src/Base_Stats.c", "strings/Pokemon_Name_Table.string", "charmap.tbl",
        "scripts/string.py", "repointall",
    ],
}


class ProfileError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ProfileError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def serialized(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def run(args, *, cwd=None, source=None):
    result = subprocess.run(args, cwd=cwd, input=source, capture_output=True, text=True)
    require(result.returncode == 0, f"{args[0]} failed: {result.stderr.strip()}")
    return result.stdout


def git(root, *args):
    return run(["git", "-C", str(root), *args]).strip()


class LockedSources:
    def __init__(self, root):
        self.root = root
        self.provenance = {}
        for ref, tree in ((PRODUCT, PRODUCT_TREE), (CONTRACT, CONTRACT_TREE)):
            require(git(root, "rev-parse", f"{ref}^{{tree}}") == tree, "Workspace tree mismatch")
        for ref in (CONTRACT, "HEAD"):
            require(git(root, "rev-parse", f"{ref}:{EXTENSION}") == EXTENSION_BLOB,
                    "Unreviewed extension revision")
        for component, (path, pin) in PINS.items():
            for ref in (PRODUCT, CONTRACT, "HEAD"):
                require(git(root, "ls-tree", ref, "--", path) == f"160000 commit {pin}\t{path}",
                        f"{component}: incompatible Gitlink at {ref}")
            require(git(root / path, "rev-parse", "HEAD") == pin, f"{component}: checkout revision mismatch")

    def read(self, component, path):
        require(path in INPUTS.get(component, []), "Input is not public-source allowlisted")
        directory, pin = PINS[component]
        raw = subprocess.run(["git", "-C", str(self.root / directory), "show", f"{pin}:{path}"],
                             capture_output=True, check=True).stdout
        locator = f"{component}:{path}"
        self.provenance[locator] = {"revision": pin, "sha256": digest(raw)}
        return raw.decode("utf-8-sig")


def uncomment(text):
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)


def select_conditionals(text, flags):
    """Restricted preprocessing; no include traversal or evaluation of unknown #if."""
    active = True
    stack = []
    result = []
    for line in uncomment(text).splitlines():
        directive = re.match(r"\s*#(ifdef|ifndef)\s+(\w+)\s*$", line)
        if directive:
            op, name = directive.groups()
            require(name in flags, f"Unreviewed configuration conditional: {name}")
            condition = flags[name] if op == "ifdef" else not flags[name]
            stack.append((active, condition, False))
            active = active and condition
        elif re.match(r"\s*#else\s*$", line):
            require(stack and not stack[-1][2], "Invalid #else")
            parent, condition, _ = stack[-1]
            stack[-1] = (parent, condition, True)
            active = parent and not condition
        elif re.match(r"\s*#endif\s*$", line):
            require(stack, "Unmatched #endif")
            active = stack.pop()[0]
        elif re.match(r"\s*#(?:if|elif)\b", line):
            raise ProfileError("Unsupported conditional expression")
        elif active:
            result.append(line)
    require(not stack, "Unterminated conditional")
    return "\n".join(result)


def eval_expr(expr, symbols):
    """Integer-only C constant subset, evaluated without Python eval."""
    try:
        tree = ast.parse(expr.strip(), mode="eval").body
    except SyntaxError as error:
        raise ProfileError(f"Invalid constant expression: {expr}") from error

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.Name):
            require(node.id in symbols, f"Missing definition: {node.id}")
            return symbols[node.id]
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            a, b = visit(node.left), visit(node.right)
            return a + b if isinstance(node.op, ast.Add) else a - b
        raise ProfileError(f"Unsupported constant expression: {expr}")
    return visit(tree)


def parse_header(text, flags=None):
    text = select_conditionals(text, flags or {})
    expressions = {}
    in_enum = False
    previous = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line == "#pragma once" or line.startswith("#include "):
            continue
        if re.match(r"#define (ITEM_TO_BERRY|IS_POKEMON_ITEM)\(", line):
            continue  # Function-like helpers, not item IDs.
        if re.fullmatch(r"enum(?:\s+\w+)?(?:\s*\{)?", line):
            require(not in_enum, "Nested enum")
            in_enum, previous = True, None
            continue
        if in_enum:
            if line == "{":
                continue
            if line == "};":
                in_enum = False
                continue
            match = re.fullmatch(r"(\w+)(?:\s*=\s*(.*?))?,?", line)
            require(match, f"Invalid enum member: {line}")
            name, expr = match.groups()
            expr = expr or (f"{previous} + 1" if previous else "0")
            previous = name
        else:
            match = re.fullmatch(r"#define\s+(\w+)\s+(.+)", line)
            require(match, f"Unsupported header definition: {line}")
            name, expr = match.groups()
        require(name not in expressions, f"Duplicate definition: {name}")
        expressions[name] = expr
    require(not in_enum, "Unterminated enum")
    symbols = {}
    pending = dict(expressions)
    while pending:
        resolved = []
        for name, expr in pending.items():
            try:
                symbols[name] = eval_expr(expr, symbols)
                resolved.append(name)
            except ProfileError:
                pass
        require(resolved, f"Unresolved definitions: {sorted(pending)}")
        for name in resolved:
            del pending[name]
    return symbols, expressions


def charmap(text):
    encode, decode = {}, {}
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9A-Fa-f]{2})=(.+)", line)
        if not match:
            continue
        code, char = match.groups()
        value = int(code, 16)
        encode[char] = value
        if len(char) == 1:
            # Source map accepts typographic and ASCII spellings of these glyphs.
            char = {"“": '"', "’": "'"}.get(char, char)
            require(value not in decode or decode[value] == char, "Ambiguous character map")
            decode[value] = char
    return encode, decode


def decode_bytes(values, decode):
    require(all(value in decode for value in values), "Unsupported name character byte")
    return "".join(decode[value] for value in values)


def parse_strings(text, table, encoding):
    encode, decode = charmap(encoding)
    length = re.findall(r"^MAX_LENGTH=(\d+)$", text, re.M)
    require(len(length) == 1 and "FILL_FF=True" in text, "Missing fixed string layout")
    length = int(length[0])
    rows, labels = [], []
    seen = set()
    for line in text.splitlines():
        if not line or line.startswith("//") or line.startswith(("MAX_LENGTH=", "FILL_FF=")):
            continue
        if line.startswith("#org @"):
            label = line[6:]
            require(label not in seen, f"Duplicate string label: {label}")
            seen.add(label)
            labels.append(label)
            continue
        require(labels and not line.startswith("#"), "Unsupported string directive or unlabelled row")
        tokens = re.findall(r"\[[^]]*\]|\\.|.", line)
        values = []
        for token in tokens:
            if re.fullmatch(r"\[[0-9A-Fa-f]{2}\]", token):
                values.append(int(token[1:-1], 16))
            else:
                require(token in encode, f"Unknown string token: {token}")
                values.append(encode[token])
        # Match the source converter's explicit truncation, retaining the original.
        rows.append({"labels": labels, "name": decode_bytes(values[:length], decode),
                     "sourceText": line, "truncated": len(values) > length})
        labels = []
    require(not labels and rows and rows[0]["labels"][0] == table, "Invalid string table start/end")
    return rows, length + 1


def id_symbols(symbols, prefix):
    return {key: value for key, value in symbols.items() if key.startswith(prefix)
            and not key.endswith("_NAME_LENGTH") and not key.startswith("ITEM_USE_")}


def mapping(symbols, expressions, prefix, count, names, *, selected=None, sentinels=()):
    require(type(count) is int and count > 0, "Missing/invalid required table bound")
    require(len(names) == count, "Name table length differs from explicit bound")
    groups = {}
    for key, value in id_symbols(symbols, prefix).items():
        require(0 <= value < count, f"ID outside declared table: {key}")
        groups.setdefault(value, []).append(key)
    rows = []
    for value in range(count):
        constants = sorted(groups.get(value, []))
        aliases = []
        if constants:
            roots = [k for k in constants if expressions[k].strip("() ") not in constants]
            if selected is not None:
                canonical = selected[value]
                require(canonical in constants, f"Table designator/id mismatch at {value}")
                # Multiple literal spellings are only authoritative when the source row selects one.
            else:
                require(len(roots) == 1, f"Ambiguous duplicate ID {value}: {constants}")
                canonical = roots[0]
            aliases = [{"constant": k, "sourceExpression": expressions[k]} for k in constants if k != canonical]
            state = "sentinel" if canonical in sentinels else "mapped"
        else:
            canonical, state = None, "hole"
        rows.append({"id": value, "constant": canonical, "aliases": aliases,
                     "sourceExpression": expressions[canonical] if canonical else None,
                     "state": state, **names[value]})
    return rows


def array_body(text, symbol):
    match = re.search(r"\b" + re.escape(symbol) + r"\s*\[\s*\]\s*=\s*\{", text)
    require(match, f"Missing source table: {symbol}")
    depth, start = 1, match.end()
    for index in range(start, len(text)):
        depth += (text[index] == "{") - (text[index] == "}")
        if depth == 0:
            return text[start:index]
    raise ProfileError(f"Unterminated table: {symbol}")


def item_names(text, symbols, easy, encoding):
    body = array_body(uncomment(text), "gItemData")
    require("#" not in body, "Conditional item table requires review")
    easy_symbols, _ = parse_header(re.sub(r"^#define _BUFFER.*$", "", easy, flags=re.M))
    _, decode = charmap(encoding)
    rows, selected = [], []
    depth, start, between = 0, None, ""
    for i, char in enumerate(body):
        if char == "{":
            if depth == 0:
                designator = between.strip().lstrip(",").strip()
                if designator:
                    match = re.fullmatch(r"\[(\w+)\]\s*=?", designator)
                    require(match and symbols.get(match[1]) == len(rows), "Invalid/nonsequential item designator")
                between = ""
                start = i + 1
            depth += 1
        elif char == "}":
            depth -= 1
            require(depth >= 0, "Invalid item braces")
            if depth == 0:
                row = body[start:i]
                ids = re.findall(r"\.itemId\s*=\s*(\w+)\s*,", row)
                names = re.findall(r"\.name\s*=\s*\{([^}]+)\}", row)
                require(len(ids) == len(names) == 1, "Missing/duplicate item ID/name")
                require(symbols.get(ids[0]) == len(rows), f"Item row/index mismatch: {ids[0]}")
                tokens = [s.strip() for s in names[0].split(",") if s.strip()]
                require(tokens and tokens[-1] == "_END" and len(tokens) <= 14, "Invalid item name termination/width")
                values = [eval_expr(token, easy_symbols) for token in tokens[:-1]]
                rows.append({"name": decode_bytes(values, decode), "labels": [ids[0]],
                             "sourceText": names[0].strip(), "truncated": False})
                selected.append(ids[0])
        elif depth == 0:
            between += char
    require(depth == 0 and not between.strip().strip(","), "Unterminated item row")
    return rows, selected


def record(text, kind, name):
    found = re.findall(r"\b" + kind + r"\s+" + name + r"\s*\{([^{}]+)\}", text, re.S)
    require(len(found) == 1, f"Missing/ambiguous {kind} {name}")
    require("#" not in found[0], f"Conditional layout: {name}")
    return f"{kind} {name} {{" + found[0] + "};\n"


def derive_layouts(cfru, dpe, clang):
    pokemon = cfru["include/pokemon.h"]
    battle = cfru["include/battle.h"]
    global_h = cfru["include/global.h"]
    primitive = cfru["include/gba/types.h"]
    for alias, target in (("u8", "uint8_t"), ("u16", "uint16_t"), ("u32", "uint32_t"),
                          ("s8", "int8_t"), ("bool8", "u8")):
        require(re.search(r"typedef\s+" + target + r"\s+" + alias + r"\s*;", primitive), "Changed primitive typedef")
    macros = []
    for name, source in (("BATTLE_STATS_NO", pokemon), ("POKEMON_NAME_LENGTH", global_h)):
        found = re.findall(r"^#define\s+" + name + r"\s+(\d+)\s*$", source, re.M)
        require(len(found) == 1, f"Missing layout constant {name}")
        macros.append(f"#define {name} {found[0]}\n")
    names = ["Pokemon", "BattlePokemon", "BaseStats", "BattleMove",
             "TrainerMonNoItemDefaultMoves", "TrainerMonItemDefaultMoves",
             "TrainerMonNoItemCustomMoves", "TrainerMonItemCustomMoves", "Trainer", "Item"]
    locations = {name: "include/" + ("pokemon.h" if name in names[:4] else
                 "item.h" if name == "Item" else "battle.h") for name in names}
    records = {name: record(cfru[locations[name]], "struct", name) for name in names}
    require(uncomment(records["BaseStats"]).split() ==
            uncomment(record(dpe["include/base_stats.h"], "struct", "BaseStats")).split(),
            "DPE/CFRU BaseStats layouts disagree")
    prelude = "typedef unsigned char u8; typedef signed char s8; typedef unsigned short u16; typedef unsigned int u32; typedef u8 bool8;\n"
    require("typedef void (*ItemUseFunc)(u8);" in cfru["include/item.h"], "Changed ItemUseFunc type")
    prelude += "typedef void (*ItemUseFunc)(u8);\n"
    # Standalone declarations only. No source includes, objects, build tree or host ABI.
    unit = prelude + "".join(macros) + "".join(records[n] for n in names if n != "Trainer")
    unit += record(battle, "union", "TrainerMonPtr") + records["Trainer"]
    unit += '_Static_assert(sizeof(void*) == 4, "GBA pointer width");\n'
    dump = run([clang, "-cc1", "-triple", "thumbv4t-none-eabi", "-std=c11",
                "-ffreestanding", "-Werror", "-fsyntax-only", "-fdump-record-layouts-complete", "-x", "c", "-"], source=unit)
    layouts = {}
    for name in names:
        match = re.search(r"^\s*0 \| struct " + name + r"\n(.*?)(?=\n\n|\Z)", dump, re.M | re.S)
        require(match, f"No target ABI proof: {name}")
        size = re.search(r"\[sizeof=(\d+), align=(\d+)\]", match[1])
        require(size, "Unrecognized target layout output")
        fields = {}
        for line in match[1].splitlines():
            field = re.fullmatch(r"\s*(\d+)(?::(\d+)-(\d+))? \|   (\S.*?\s)(\w+)", line)
            if field:
                offset, bit_start, bit_end, c_type, member = field.groups()
                fields[member] = {"offset": int(offset), "type": c_type.strip()}
                if bit_start is not None:
                    fields[member].update(bitOffset=int(bit_start), bitWidth=int(bit_end) - int(bit_start) + 1)
        require(fields, f"No fields parsed: {name}")
        require(len(fields) == uncomment(records[name]).count(";") - 1,
                f"Incomplete field extraction: {name}")
        layouts[name] = {"size": int(size[1]), "alignment": int(size[2]), "fields": fields,
                         "source": "CFRU:" + locations[name] + "::" + name,
                         "declarationSha256": digest(records[name].encode())}
    expected = {"Pokemon": (100, {"species": 32, "moves": 44, "condition": 80, "hp": 86}),
                "BattlePokemon": (88, {"ability": 32, "moves": 12, "status1": 76}),
                "BaseStats": (28, {"hiddenAbility": 26}), "BattleMove": (12, {"split": 10}),
                "Trainer": (40, {"party": 36}), "TrainerMonItemCustomMoves": (32, {"heldItem": 20, "moves": 22, "teraType": 30}),
                "Item": (44, {"itemId": 14, "description": 20, "battleUseFunc": 36})}
    for name, (size, offsets) in expected.items():
        require(layouts[name]["size"] == size, f"Unreviewed target size: {name}")
        for member, offset in offsets.items():
            require(layouts[name]["fields"].get(member, {}).get("offset") == offset, f"Unreviewed target field: {name}.{member}")
    required_types = {
        "Pokemon": {"personality": "u32", "species": "u16", "item": "u16", "moves": "u16[4]",
                    "pp": "u8[4]", "condition": "u32", "hp": "u16", "maxHP": "u16"},
        "BattlePokemon": {"species": "u16", "moves": "u16[4]", "ability": "u8", "status1": "u32"},
        "BattleMove": {"split": "u8"}, "BaseStats": {"hiddenAbility": "u8"},
    }
    for name, members in required_types.items():
        for member, c_type in members.items():
            require(layouts[name]["fields"].get(member, {}).get("type") == c_type,
                    f"Unreviewed field width: {name}.{member}")
    hidden = layouts["Pokemon"]["fields"]["hiddenAbility"]
    require(hidden == {"offset": 75, "type": "u32", "bitOffset": 7, "bitWidth": 1},
            "Unreviewed hidden-ability bitfield")
    return {"target": "thumbv4t-none-eabi", "endianness": "little", "pointerBytes": 4,
            "proof": "Clang ARM target record layout of source-extracted declarations; syntax only, no objects",
            "translationUnitSha256": digest(unit.encode()), "records": layouts}


def address_descriptors(cfru, dpe):
    result = {}
    for declaration in ("extern u32 gBattleTypeFlags;", "extern u8 gBattlersCount;",
                        "extern u16 gBattlerPartyIndexes[MAX_BATTLERS_COUNT];"):
        require(declaration in cfru["include/battle.h"], "Changed RAM symbol type")
    require(re.search(r"#define\s+gTrainerBattleOpponent_B\s+ExtensionState.trainerBTrainerId\b",
                      cfru["include/new/multi.h"]), "Changed trainer-B source binding")
    for symbol, width in (("gPlayerParty", 1), ("gEnemyParty", 1), ("gPlayerPartyCount", 1),
                          ("gBattleMons", 1), ("gBattlerPartyIndexes", 2),
                          ("gBattleTypeFlags", 4), ("gBattlersCount", 1)):
        matches = re.findall(r"^" + symbol + r"\s*=\s*(0x[\da-fA-F]+);", cfru["BPRE.ld"], re.M)
        require(len(matches) == 1, f"Missing fixed source symbol {symbol}")
        address = int(matches[0], 16)
        require(0x02000000 <= address < 0x02040000 and address % width == 0, "Invalid source RAM domain/alignment")
        result[symbol] = {"kind": "fixed-symbol", "source": "CFRU:BPRE.ld::" + symbol,
                          "sourceAddress": address, "domain": "EWRAM", "widthBytes": width,
                          "indirection": 0, "runtimeAddress": "UNRESOLVED"}
    for component, source, symbols in (("CFRU", cfru, ["gBattleMoves", "gMoveNames", "gAbilityNames", "gItemData"]),
                                        ("DPE", dpe, ["gBaseStats", "gSpeciesNames"])):
        for symbol in symbols:
            matches = re.findall(r"^" + symbol + r"\s+([\da-fA-F]{8})\s*$", source["repointall"], re.M)
            require(len(matches) == 1, f"Missing repoint anchor: {symbol}")
            result[symbol] = {"kind": "repoint-anchor", "source": f"{component}:repointall::{symbol}",
                              "sourceAddress": int(matches[0], 16), "domain": "ROM", "widthBytes": 4,
                              "indirection": None, "runtimeAddress": "UNRESOLVED"}
    for symbol in ("gBaseStats", "gSpeciesNames", "gItems"):
        lines = [line for line in cfru["include/new/rom_locs.h"].splitlines() if line.startswith("#define " + symbol + " ")]
        require(len(lines) == 1 and "*((u32*)" in lines[0], f"Missing source pointer slot {symbol}")
        matches = re.findall(r"0x[0-9a-fA-F]+", lines[0])
        require(len(matches) == 1, "Ambiguous pointer-slot source")
        result[symbol + "PointerSlot"] = {"kind": "pointer-slot", "symbol": symbol,
            "source": "CFRU:include/new/rom_locs.h::" + symbol, "sourceAddress": int(matches[0], 16),
            "domain": "ROM", "widthBytes": 4, "indirection": 1, "runtimeAddress": "UNRESOLVED"}
    result["gTrainerBattleOpponent_B"] = {"kind": "UNRESOLVED", "domain": "EWRAM",
        "widthBytes": 2, "indirection": None, "runtimeAddress": "UNRESOLVED",
        "source": "CFRU:include/new/multi.h::gTrainerBattleOpponent_B",
        "reason": "ExtensionState.trainerBTrainerId requires independently validated extension-state binding"}
    result["gTrainerBattleOpponent_A"] = {"kind": "UNRESOLVED", "domain": "EWRAM",
        "widthBytes": 2, "indirection": None, "runtimeAddress": "UNRESOLVED",
        "source": "CFRU:src/build_pokemon.c::BuildTrainerPartySetup",
        "reason": "No independently established address in the selected source descriptors"}
    for descriptor in result.values():
        descriptor["validation"] = ["local-output binding", "session identity", "domain/bounds/alignment", "field sanity"]
        if descriptor["domain"] == "ROM":
            address = descriptor["sourceAddress"]
            require(0x08000000 <= address < 0x0A000000 and address % 4 == 0, "Invalid source ROM domain/alignment")
    return result


def make_profile(reader, clang="clang"):
    sources = {component: {path: reader.read(component, path) for path in paths} for component, paths in INPUTS.items()}
    c, d = sources["CFRU"], sources["DPE"]
    config = select_conditionals(c["src/config.h"], {"IgnoreWildPokemon": False})
    flags = {name: bool(re.search(r"^#define\s+" + name + r"(?:\s|$)", config, re.M))
             for name in ("UNBOUND", "EXPANDED_NEW_ITEMS")}
    require(flags == {"UNBOUND": False, "EXPANDED_NEW_ITEMS": True}, "Unsupported item configuration")
    for flag in ("ACTUAL_PLA_MOVE_POWERS", "BUFFED_LEECH_LIFE", "DARK_VOID_ACC_NERF",
                 "GEN_6_POWER_NERFS", "GEN_7_POWER_NERFS", "FROSTBITE", "DYNAMAX_FEATURE"):
        flags[flag] = bool(re.search(r"^#define\s+" + flag + r"(?:\s|$)", config, re.M))
    headers = {}
    for kind in ("species", "moves", "abilities", "items"):
        headers[kind] = (parse_header(c[f"include/constants/{kind}.h"], flags),
                         parse_header(d[f"include/{kind}.h"], flags))
    tables, counts = {}, {}
    # Reviewed spelling/slot differences, not proof of equivalent mechanics.
    cross_names = {
        "SPECIES_OGERPON_TERASTAL": (1426, "SPECIES_OGERPON_GREEN"),
        "SPECIES_OGERPON_WELLSPRING_TERASTAL": (1427, "SPECIES_OGERPON_BLUE"),
        "SPECIES_OGERPON_HEARTHFLAME_TERASTAL": (1428, "SPECIES_OGERPON_RED"),
        "SPECIES_OGERPON_CORNERSTONE_TERASTAL": (1429, "SPECIES_OGERPON_GREY"),
        "ABILITY_UNUSED": (77, "ABILITY_LINGERINGAROMA"),
    }
    for kind, prefix, bound, names_path, owner, sentinel in (
        ("species", "SPECIES_", "NUM_SPECIES", "strings/Pokemon_Name_Table.string", d, ("SPECIES_NONE", "SPECIES_EGG")),
        ("moves", "MOVE_", "MOVES_COUNT", "strings/attack_name_table.string", c, ("MOVE_NONE",)),
        ("abilities", "ABILITY_", "ABILITIES_COUNT", "strings/ability_name_table.string", c, ("ABILITY_NONE",))):
        (cs, ce), (ds, de) = headers[kind]
        for key, value in id_symbols(ds, prefix).items():
            if cs.get(key) != value:
                alternate = cross_names.get(key)
                require(alternate and alternate[0] == value and cs.get(alternate[1]) == value,
                        f"CFRU/DPE ID mismatch: {key}")
        count = cs.get(bound)
        require(count is not None, f"Missing required {bound}")
        if kind != "abilities":
            require(ds.get(bound) == count, f"CFRU/DPE bound mismatch: {bound}")
        names, stride = parse_strings(owner[names_path], {"species": "gSpeciesNames", "moves": "gMoveNames", "abilities": "gAbilityNames"}[kind], owner["charmap.tbl"])
        if kind == "abilities":
            require(len(names) > count and names[count]["labels"] == ["NAME_LAST_ABILITY"], "Missing ability terminator")
            dynamic = names[count + 1:]
            names = names[:count]
        tables[kind] = mapping(cs, ce, prefix, count, names, sentinels=sentinel)
        for key, (value, target) in cross_names.items():
            if key.startswith(prefix):
                tables[kind][value]["aliases"].append({"constant": key, "sourceExpression": de[key],
                    "source": f"DPE:include/{kind}.h", "reason": "Same numeric slot; CFRU table owns effective identity"})
        counts[kind] = {"value": count, "expression": ce[bound], "source": f"CFRU:include/constants/{kind}.h::{bound}",
                        "namesSource": ("DPE:" if kind == "species" else "CFRU:") + names_path,
                        "nameStride": stride, "holes": [r["id"] for r in tables[kind] if r["state"] == "hole"]}
    (cs, ce), (ds, de) = headers["items"]
    names, selected = item_names(c["src/Tables/item_tables.c"], cs, c["include/easy_text.h"], c["charmap.tbl"])
    count = cs.get("ITEMS_COUNT")
    tables["items"] = mapping(cs, ce, "ITEM_", count, names, selected=selected, sentinels=("ITEM_NONE",))
    for row in tables["items"]:
        if row["constant"].startswith("ITEM_FREE_SPACE"):
            row["state"] = "reserved"
    require(ds.get("ITEMS_COUNT") is not None, "Missing DPE item bound")
    excluded = []
    for key, value in id_symbols(ds, "ITEM_").items():
        if value >= count:
            require(key.startswith("ITEM_SHINY_SPACE") and value < ds["ITEMS_COUNT"], "Unreviewed DPE-only item")
            excluded.append({"constant": key, "id": value, "state": "UNAVAILABLE", "reason": "No CFRU gItemData row"})
        else:
            require(cs.get(key) == value, f"Item mapping conflict: {key}")
    require(sorted(r["id"] for r in excluded) == list(range(count, ds["ITEMS_COUNT"])), "Unexplained DPE item gap")
    counts["items"] = {"value": count, "expression": ce["ITEMS_COUNT"], "source": "CFRU:include/constants/items.h::ITEMS_COUNT",
                       "table": "CFRU:src/Tables/item_tables.c::gItemData", "dpeSlots": ds["ITEMS_COUNT"], "holes": []}
    type_text = "\n".join(line for line in c["include/pokemon.h"].splitlines()
                            if re.match(r"#define\s+(TYPE_\w+|NUMBER_OF_MON_TYPES)\s", line))
    ts, te = parse_header(type_text)
    dts, _ = parse_header("\n".join(line for line in d["include/base_stats.h"].splitlines() if line.startswith("#define TYPE_")))
    require(id_symbols(ts, "TYPE_") == dts, "Type ID disagreement")
    names, stride = parse_strings(c["strings/type_names.string"], "gTypeNames", c["charmap.tbl"])
    tables["types"] = mapping(ts, te, "TYPE_", ts["NUMBER_OF_MON_TYPES"], names,
                              sentinels=("TYPE_MYSTERY", "TYPE_ROOSTLESS", "TYPE_BLANK"))
    counts["types"] = {"value": ts["NUMBER_OF_MON_TYPES"], "expression": te["NUMBER_OF_MON_TYPES"],
                       "source": "CFRU:include/pokemon.h::NUMBER_OF_MON_TYPES", "nameStride": stride,
                       "namesSource": "CFRU:strings/type_names.string",
                       "holes": [r["id"] for r in tables["types"] if r["state"] == "hole"]}
    # Coverage of C designated tables is distinct from name/ID bounds.
    coverage = {}
    for kind, text, symbol, prefix in (("species", d["src/Base_Stats.c"], "gBaseStats", "SPECIES_"),
                                       ("moves", c["src/Tables/battle_moves.c"], "gBattleMoves", "MOVE_")):
        body = array_body(select_conditionals(text, flags), symbol)
        require("#" not in body, f"Conditional {symbol} requires review")
        keys = re.findall(r"\[([^]]+)\]\s*=", body)
        require(all(re.fullmatch(prefix + r"\w+", key) for key in keys),
                f"Unreviewed designator in {symbol}")
        sy = headers[kind][1 if kind == "species" else 0][0]
        ids = [sy.get(key) for key in keys]
        require(None not in ids and len(set(ids)) == len(ids), f"Invalid/duplicate designators in {symbol}")
        mapped = {r["id"] for r in tables[kind] if r["state"] != "hole"}
        absent = ({sy[k] for k in ("SPECIES_SHADOW_WARRIOR", "SPECIES_ZYGARDE_CELL", "SPECIES_ZYGARDE_CORE")}
                  if kind == "species" else set())
        require(set(ids) == mapped - absent, f"Missing/extra {symbol} rows")
        for value in absent:
            tables[kind][value]["baselineData"] = "UNAVAILABLE"
            tables[kind][value]["reason"] = "No explicit gBaseStats initializer; implicit zero row is not a supported species"
        coverage[symbol] = {"explicitRows": len(ids), "bound": counts[kind]["value"],
                            "implicitZeroHoles": sorted(set(counts[kind]["holes"]) | absent)}
    for kind in tables:
        counts[kind]["mappedValues"] = sum(row["state"] != "hole" for row in tables[kind])
    layouts = derive_layouts(c, d, clang)
    addresses = address_descriptors(c, d)
    limits = {}
    for name, path in (("PARTY_SIZE", "include/pokemon.h"), ("MAX_BATTLERS_COUNT", "include/constants/battle.h")):
        found = re.findall(r"^#define\s+" + name + r"\s+(\d+)\s*$", c[path], re.M)
        require(len(found) == 1, f"Missing required limit {name}")
        limits[name] = {"value": int(found[0]), "source": "CFRU:" + path + "::" + name}
    capabilities = {}
    for field, dependencies, contexts, reason in (
        ("baselineNamesAndIds", ["species", "moves", "abilities", "items", "types"], ["source-baseline"], "Table names only; aliased ability display needs species/effective types"),
        ("effectiveSpecies", ["species", "types", "BaseStats", "gBaseStats"], ["validated-output"], "Randomized values require bound output"),
        ("effectiveMoves", ["moves", "types", "BattleMove", "gBattleMoves"], ["validated-output"], "Category is BattleMove.split byte"),
        ("playerParty", ["species", "moves", "items", "Pokemon", "gPlayerParty", "gPlayerPartyCount"], ["party"], "Direct CFRU fields; no vanilla XOR/shuffle"),
        ("enemyParty", ["species", "moves", "items", "Pokemon", "gEnemyParty"], ["encounter"], "Encounter construction/context must be validated in T4"),
        ("partyAbility", ["abilities", "BaseStats", "Pokemon", "gBaseStats"], ["party"], "GetMonAbility/TryRandomizeAbility and GetAbilityNameOverride require T3 semantics"),
        ("battle", ["species", "moves", "abilities", "items", "types", "BattlePokemon", "gBattleMons", "gBattlerPartyIndexes", "gBattleTypeFlags", "gBattlersCount"], ["battle"], "Context/epoch/battler-side validation required in T4")):
        capabilities[field] = {"dependencies": dependencies, "contexts": contexts, "confidence": "UNKNOWN",
                               "sampleEpoch": None, "reason": reason, "sourceOnly": True,
                               "applicability": "locked source profile; local output/session acceptance required for live use"}
    capability_sources = {
        "baselineNamesAndIds": ["counts.*.source", "counts.*.namesSource", "counts.items.table"],
        "effectiveSpecies": ["DPE:src/Base_Stats.c::gBaseStats"],
        "effectiveMoves": ["CFRU:src/Tables/battle_moves.c::gBattleMoves"],
        "playerParty": ["CFRU:include/pokemon.h::Pokemon"],
        "enemyParty": ["CFRU:src/build_pokemon.c::CreateNPCTrainerParty"],
        "partyAbility": ["CFRU:src/build_pokemon.c::GetMonAbility", "CFRU:src/util.c::TryRandomizeAbility",
                         "CFRU:src/ability_util.c::GetAbilityNameOverride"],
        "battle": ["CFRU:include/pokemon.h::BattlePokemon", "CFRU:include/battle.h::gBattlerPartyIndexes"],
    }
    for field, locators in capability_sources.items():
        capabilities[field]["sources"] = locators
    payload = {"metadata": {"schema": SCHEMA, "schemaVersion": VERSION, "evidence": "source-only",
        "productWorkspace": {"commit": PRODUCT, "tree": PRODUCT_TREE},
        "contractWorkspace": {"commit": CONTRACT, "tree": CONTRACT_TREE},
        "revisions": {key: pin for key, (_, pin) in PINS.items()},
        "generator": {"path": GENERATOR, "sha256": digest(Path(__file__).read_bytes())},
        "extensionCompatibility": {"workspaceCommit": CONTRACT, "path": EXTENSION,
            "gitBlob": EXTENSION_BLOB, "runtimeSchemaSupport": "UNRESOLVED",
            "reason": "T1 schema v2; runtime validator/activation pending T2; legacy Lua import is not acceptance"},
        "numericEncoding": "JSON integers are decimal; no numeric strings",
        "nameAssociation": "Physical source string-row index; labels are provenance, not ID heuristics",
        "configuration": {**flags, "source": "CFRU:src/config.h", "externalOverrides": "unsupported"},
        "inputs": reader.provenance},
        "counts": counts, **tables, "tableCoverage": coverage, "limits": limits,
        "itemExclusions": sorted(excluded, key=lambda row: row["id"]),
        "abilityNameOverrides": {"names": dynamic, "source": "CFRU:src/ability_util.c::GetAbilityNameOverride",
            "resolution": "UNRESOLVED", "reason": "Context-dependent species/effective-type rules; table name is baseline only",
            "tableTerminator": {"id": counts["abilities"]["value"], "label": "NAME_LAST_ABILITY", "state": "sentinel-outside-ID-bound"}},
        "layouts": layouts, "addresses": addresses, "capabilities": capabilities,
        "limitations": ["No runtime/output identity binding or emulator/UI compatibility",
            "Ability aliases/names do not certify mechanics or effective contextual names",
            "DPE-only shiny item slots and CFRU free-space rows are not usable items",
            "No stock resources, national-dex/form normalization, sprites or derived damage data inferred"]}
    payload["metadata"]["profileId"] = "sha256:" + digest(serialized(payload))
    return payload


def validate_profile(value, expected):
    """Public source validator: exact regenerated contract, including unknown keys.

    A recomputed self hash alone cannot authorize changed pins, layouts or mappings.
    Runtime bindings have a separate, not-yet-implemented T2 validator.
    """
    require(type(value) is dict and type(value.get("metadata")) is dict, "Missing profile metadata")
    metadata = value["metadata"]
    require(metadata.get("schema") == SCHEMA and type(metadata.get("schemaVersion")) is int
            and metadata["schemaVersion"] == VERSION, "Unsupported schema")
    require(serialized(value) == serialized(expected), "Profile differs from regenerated locked source contract")


def generate(source_root, clang="clang"):
    return make_profile(LockedSources(Path(source_root).resolve()), clang)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path(OUTPUT))
    parser.add_argument("--clang", default="clang", help="Clang with ARM target syntax support (no objects emitted)")
    parser.add_argument("--check", action="store_true", help="Verify committed output byte-for-byte without writing")
    args = parser.parse_args()
    try:
        data = generate(args.source_root, args.clang)
        output = args.output if args.output.is_absolute() else args.source_root / args.output
        if args.check:
            raw = output.read_bytes()
            validate_profile(json.loads(raw), data)
            require(raw == serialized(data), "Non-deterministic serialization")
            print("PASS: source profile matches locked inputs byte-for-byte")
        else:
            output.write_bytes(serialized(data))
            print("Generated source-only profile: " + data["metadata"]["profileId"])
        return 0
    except (ProfileError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
