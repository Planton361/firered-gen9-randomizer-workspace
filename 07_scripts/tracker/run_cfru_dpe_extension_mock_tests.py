#!/usr/bin/env python3
"""Run ROM-free Lua mock tests using installed runtimes only; no installation.

Exit 2 / NOT_RUN if no supported runtime exists. Source checks are independent.
Public JSON is converted to an in-memory fixture (not a local runtime manifest).
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def lua_literal(value):
    if value is None:
        return "nil"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "{" + ",".join(lua_literal(v) for v in value) + "}"
    return "{" + ",".join("[" + lua_literal(k) + "]=" + lua_literal(v)
                          for k, v in value.items()) + "}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lua", help="Already installed Lua 5.1/5.4 executable; never downloaded")
    args = parser.parse_args()
    names = [args.lua] if args.lua else ["lua5.1", "lua51", "lua5.4", "lua54", "lua", "luajit"]
    runtimes = []
    for name in names:
        executable = shutil.which(name)
        if executable and executable not in runtimes:
            runtimes.append(executable)
    if not runtimes:
        print("NOT_RUN: Lua mock/syntax/SHA-256 tests; no installed Lua 5.1/5.4 runtime")
        print("CFRUDPE_EXTENSION_PROFILE_MOCK_GUARD_READY: NOT_ESTABLISHED")
        return 2
    raw = (ROOT / "03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json").read_text()
    vectors = [["a" * n, hashlib.sha256(b"a" * n).hexdigest()] for n in [55, 56, 63, 64, 65, 128]]
    chunk = "MOCK_SOURCE=" + lua_literal(raw) + "\nMOCK_PROFILE=" + lua_literal(json.loads(raw))
    chunk += "\nMOCK_SHA_VECTORS=" + lua_literal(vectors)
    chunk += '\ndofile("07_scripts/tracker/tests/cfru_dpe_extension_mock.lua")\n'
    tested = set()
    for runtime in runtimes:
        probe = subprocess.run([runtime, "-e", "io.write(_VERSION)"], text=True, capture_output=True, check=False)
        version = probe.stdout
        if probe.returncode or version not in {"Lua 5.1", "Lua 5.4"}:
            print("NOT_RUN:", runtime, "is not a working Lua 5.1/5.4 runtime")
            continue
        result = subprocess.run([runtime, "-"], input=chunk, text=True, cwd=ROOT, check=False)
        if result.returncode:
            print("FAIL:", version, "mock suite")
            return 1
        tested.add(version)
    for version in sorted({"Lua 5.1", "Lua 5.4"} - tested):
        print("NOT_RUN:", version, "compatibility runtime unavailable")
    if not tested:
        return 2
    print("PASS: available runtime mock suite; source/safety gates must be checked separately")
    return 0


if __name__ == "__main__":
    sys.exit(main())
