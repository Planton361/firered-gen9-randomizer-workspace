#!/usr/bin/env python3
"""ROM-free read-only audit of exact Git objects; never use dirty component files."""
import argparse
import ast
import json
import re
import subprocess
from pathlib import Path

DPE_PIN = "22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc"
CFRU_PIN = "827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec"
SYNC_CFRU = "8c2d69b48aee8923098912ee06c188d3db93d231"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True)


def clean(text):
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)


def constants(text):
    raw = dict(re.findall(r"^#define\s+(\w+)\s+([^\n]+)", clean(text), re.M))
    resolved = {}
    def value(name):
        if name in resolved:
            return resolved[name]
        def visit(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, int): return node.value
            if isinstance(node, ast.Name): return value(node.id)
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
                a, b = visit(node.left), visit(node.right)
                return a+b if isinstance(node.op, ast.Add) else a-b
            raise ValueError(name)
        resolved[name] = visit(ast.parse(raw[name].strip(), mode="eval").body)
        return resolved[name]
    for name in raw:
        try: value(name)
        except (ValueError, SyntaxError, KeyError): pass
    return resolved


def learnsets(text, species, moves):
    text = clean(text)
    blocks = {}
    for name, body in re.findall(r"static const struct LevelUpMove\s+(\w+)\[\]\s*=\s*\{(.*?)\};", text, re.S):
        if name in blocks: raise ValueError("Duplicate learnset " + name)
        if body.count("LEVEL_UP_END") != 1: raise ValueError("Bad terminator " + name)
        entries = [(int(level), moves.get(move, move)) for level, move in
                   re.findall(r"LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_\w+)\)", body)]
        blocks[name] = entries
    pointers = re.findall(r"\[(SPECIES_\w+)\]\s*=\s*(\w+)", text)
    result, names = {}, {}
    for species_name, target in pointers:
        identity = species.get(species_name, species_name)
        if identity in result: raise ValueError("Duplicate species pointer " + species_name)
        result[identity] = blocks.get(target, {"missing_declaration": target})
        names[identity] = species_name
    return result, names, len(blocks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cfru-ref", default=CFRU_PIN)
    args = parser.parse_args()
    d = args.source_workspace / "02_external/Dynamic-Pokemon-Expansion-Gen-9"
    c = args.source_workspace / "02_external/CFRU-expansion"
    cfru_ref = git(c, "rev-parse", args.cfru_ref+"^{commit}").strip()
    ds = lambda path: git(d, "show", DPE_PIN+":"+path)
    cs = lambda path: git(c, "show", cfru_ref+":"+path)
    dspecies, cspecies = constants(ds("include/species.h")), constants(cs("include/constants/species.h"))
    dmoves, cmoves = constants(ds("include/moves.h")), constants(cs("include/constants/moves.h"))
    ability_source = ds("include/abilities.h")
    da, ca = constants(ability_source), constants(cs("include/constants/abilities.h"))
    assert not re.search(r"^\s*#define\s+EXPAND_LEARNSETS\b", clean(ds("src/defines.h")), re.M)
    dl, dn, db = learnsets(ds("src/Learnsets.c"), dspecies, dmoves)
    cl, cn, cb = learnsets(cs("src/Tables/level_up_learnsets.c"), cspecies, cmoves)
    stats = clean(ds("src/Base_Stats.c"))
    fields = ("baseHP", "baseAttack", "baseDefense", "baseSpeed", "baseSpAttack", "baseSpDefense")
    abilities = ("ability1", "ability2", "hiddenAbility")
    base_rows, problems, assignments = {}, [], []
    for name, body in re.findall(r"\[(SPECIES_\w+)\]\s*=\s*\{(.*?)\}\s*,", stats, re.S):
        values = dict(re.findall(r"\.(\w+)\s*=\s*([^,]+),", body))
        identity = dspecies[name]
        base_rows[identity] = name
        if name == "SPECIES_NONE": continue
        for field in fields:
            number = int(values.get(field, "0"))
            if not 0 < number <= 255:
                problems.append({"species": name, "field": field, "value": number,
                                 "classification": "OUT_OF_SCOPE" if name == "SPECIES_EGG" else "UNKNOWN"})
        for field in abilities:
            macro = values.get(field, "ABILITY_NONE").strip()
            number = da.get(macro)
            if number is None or not 0 <= number <= 254:
                problems.append({"species": name, "field": field, "value": macro, "classification": "UNKNOWN"})
            assignments.append((name,field,macro,number))
    diffs = [{"id": n, "dpe_species": dn.get(n), "cfru_species": cn.get(n),
              "dpe": dl.get(n), "cfru": cl.get(n), "classification": "OUT_OF_SCOPE",
              "reason": "DPE EXPAND_LEARNSETS disabled; current pilot uses CFRU table"}
             for n in sorted(dl.keys() | cl.keys(), key=str) if dl.get(n) != cl.get(n)]
    invalid = [{"component": label, "id": n, "classification": "OUT_OF_SCOPE" if label == "DPE" else "UNKNOWN"}
               for label, tables in (("DPE", dl), ("CFRU", cl)) for n, entries in tables.items()
               if not isinstance(entries, list) or any(not (0 <= level <= 100 and isinstance(move, int) and 0 < move < 992) for level, move in entries)]
    shared_ability_drift = {name: [da[name], ca[name]] for name in da.keys() & ca.keys()
                            if name.startswith("ABILITY_") and da[name] != ca[name]}
    shared_move_drift = {name: [dmoves[name], cmoves[name]] for name in dmoves.keys() & cmoves.keys()
                         if name.startswith("MOVE_") and dmoves[name] != cmoves[name]}
    name_text = cs("strings/ability_name_table.string")
    labels = re.findall(r"^#org @(\w+)\n([^#\n][^\n]*)", name_text, re.M)
    name_rows = [(label, name.strip()) for label, name in labels]
    ability_aliases = [{"macro": name, "id": number,
                        "classification": "INTENTIONAL_ALIAS"}
                       for name, number in sorted(da.items()) if name.startswith("ABILITY_") and
                       re.search(r"^#define\s+"+name+r"\s+ABILITY_", ability_source, re.M)]
    national = constants(cs("include/constants/pokedex.h"))
    national_table = ds("src/Species_To_Pokdex_Table.c").split("};",1)[0]
    national_mapping = [(dspecies[species],national[dex]) for species,dex in
                        re.findall(r"\[(SPECIES_\w+)\s*-\s*1\]\s*=\s*(NATIONAL_DEX_\w+)",national_table)]
    coverage = {}
    ranges = [(1,151),(152,251),(252,386),(387,493),(494,649),(650,721),(722,809),(810,905),(906,1025)]
    for gen, (lo,hi) in enumerate(ranges,1):
        found, missing = set(), []
        for identity, number in national_mapping:
            if not lo <= number <= hi: continue
            if identity in base_rows and isinstance(cl.get(identity),list) and cl[identity]: found.add(number)
        missing = sorted(set(range(lo,hi+1))-found)
        coverage[str(gen)] = {"national_species_with_base_and_active_learnset":len(found),"expected":hi-lo+1,"missing":missing}
    report = {
        "dpe_pin": DPE_PIN, "cfru_pin": cfru_ref,
        "comparison_scope": "Pinned local source consistency; external authoritative dataset absent from tracked workspace",
        "base_stat_rows": len(base_rows), "base_row_ids": [min(base_rows), max(base_rows)],
        "generation_coverage": coverage,
        "base_stat_or_ability_encoding_findings": problems,
        "ability_slots_checked": len(assignments), "shared_ability_constant_drift": shared_ability_drift,
        "ability_macros_only_dpe": sorted(da.keys()-ca.keys()),
        "ability_macros_only_cfru": sorted(ca.keys()-da.keys()),
        "assignments_using_dpe_only_ability_names": [row for row in assignments if row[2] not in ca],
        "ability_aliases": ability_aliases, "ability_name_rows": len(name_rows),
        "ability_name_encoding": "MAX_LENGTH=16 plus explicit FF terminator (17 bytes); contextual overrides follow indexed table",
        "overlength_ability_names": [(label,name) for label,name in name_rows if len(name)>16],
        "learnset_blocks": {"DPE": db,"CFRU": cb},
        "learnset_pointer_rows": {"DPE": len(dl),"CFRU": len(cl)},
        "learnset_equal_rows": sum(dl.get(n)==cl.get(n) for n in dl.keys()&cl.keys()),
        "learnset_differences": diffs, "invalid_learnset_entries": invalid,
        "maximum_learnset_length": {"DPE": max(len(v) for v in dl.values() if isinstance(v,list)),"CFRU": max(len(v) for v in cl.values() if isinstance(v,list))},
        "shared_move_constant_drift": shared_move_drift,
        "cfru_learnsets_changed_since_sync": bool(git(c,"diff","--name-only",SYNC_CFRU,cfru_ref,"--","src/Tables/level_up_learnsets.c").strip()),
        "upstream_reconciliation": "UNKNOWN: approved upstream snapshot is not tracked; no new data generated",
    }
    encoded = json.dumps(report,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    summary = {k:v for k,v in report.items() if k not in ("learnset_differences","ability_aliases","base_stat_or_ability_encoding_findings")}
    summary["base_stat_or_ability_encoding_finding_count"] = len(problems)
    summary["base_stat_or_ability_encoding_finding_samples"] = problems[:8]
    summary["learnset_difference_count"] = len(diffs)
    summary["learnset_difference_species"] = [row["dpe_species"] or row["cfru_species"] for row in diffs]
    summary["ability_alias_count"] = len(ability_aliases)
    print(json.dumps(summary,indent=2))


if __name__ == "__main__": main()
