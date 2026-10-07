#!/usr/bin/env python3
"""#692 detached source/synthetic suite; existing Lua 5.4 only, no game inputs."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import generate_cfru_dpe_source_data as source
from run_cfru_dpe_extension_mock_tests import lua_literal

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_SOURCES = {
    "DPE": ["src/Base_Stats.c"],
    "CFRU": ["src/Tables/battle_moves.c", "include/battle.h",
             "include/constants/battle.h", "include/pokemon.h"],
}


def baseline_expectations(texts, profile):
    """Transient assertions from the existing Python source parser, no new profile."""
    symbols = {}
    for kind in ("species", "moves", "abilities", "items", "types"):
        for row in profile[kind]:
            if row["constant"]:
                symbols[row["constant"]] = row["id"]
            for alias in row["aliases"]:
                symbols[alias["constant"]] = row["id"]
    symbols.update({name: int(n) for name, n in re.findall(
        r"#define\s+(SPLIT_\w+)\s+(\d+)", texts["CFRU:include/battle.h"])})
    expected = {}
    for kind, locator, symbol, fields in (
        ("species", "DPE:src/Base_Stats.c", "gBaseStats",
         ("type1", "type2", "ability1", "ability2", "hiddenAbility")),
        ("moves", "CFRU:src/Tables/battle_moves.c", "gBattleMoves",
         ("type", "power", "accuracy", "pp", "split")),
    ):
        text = source.select_conditionals(texts[locator], profile["metadata"]["configuration"])
        body = source.array_body(text, symbol)
        expected[kind] = []
        for constant, declaration in re.findall(r"\[(\w+)\]\s*=\s*\{([^{}]*)\}", body):
            value = symbols[constant]
            if profile[kind][value]["state"] != "mapped":
                continue
            assignments = dict(re.findall(r"\.(\w+)\s*=\s*([^,]+),", declaration))
            expected[kind].append({"id": value, "fields": {
                field: source.eval_expr(assignments[field], symbols) for field in fields}})
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lua", default="lua5.4", help="Existing Lua 5.4 executable")
    args = parser.parse_args()
    runtime = shutil.which(args.lua)
    if not runtime:
        print("NOT_RUN: existing Lua 5.4 unavailable")
        return 2
    probe = subprocess.run([runtime, "-e", "io.write(_VERSION)"], text=True,
                           capture_output=True, check=False)
    if probe.returncode or probe.stdout != "Lua 5.4":
        print("NOT_RUN: selected executable is not Lua 5.4")
        return 2
    reader = source.LockedSources(ROOT)
    texts = {f"{component}:{path}": reader.read(component, path)
             for component, paths in PUBLIC_SOURCES.items() for path in paths}
    raw = (ROOT / source.OUTPUT).read_text()
    profile = json.loads(raw)
    for locator, text in texts.items():
        source.require(source.digest(text.encode()) == profile["metadata"]["inputs"][locator]["sha256"],
                       "Supplemental source bytes differ from accepted T1 input")
    chunk = "MOCK_SOURCE=" + lua_literal(raw)
    chunk += "\nMOCK_PROFILE=" + lua_literal(profile)
    chunk += "\nMOCK_PUBLIC_SOURCES=" + lua_literal(texts)
    chunk += "\nMOCK_BASELINE=" + lua_literal(baseline_expectations(texts, profile))
    chunk += '\ndofile("07_scripts/tracker/tests/cfru_dpe_party_mock.lua")\n'
    result = subprocess.run([runtime, "-"], input=chunk, text=True, cwd=ROOT, check=False)
    return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
