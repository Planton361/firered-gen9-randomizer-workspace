#!/usr/bin/env python3
"""#694 detached UI projection; existing Lua 5.4 and allowlisted public sources."""
import argparse
import json
import shutil
import subprocess
import sys

import generate_cfru_dpe_source_data as source
from run_cfru_dpe_party_mock_tests import ROOT, PUBLIC_SOURCES
from run_cfru_dpe_extension_mock_tests import lua_literal


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
    multi = reader.read("CFRU", "include/new/multi.h")
    raw = (ROOT / source.OUTPUT).read_text()
    profile = json.loads(raw)
    for locator, text in {**texts, "CFRU:include/new/multi.h": multi}.items():
        source.require(source.digest(text.encode()) == profile["metadata"]["inputs"][locator]["sha256"],
                       "Source bytes differ from accepted T1 input")
    chunk = "MOCK_SOURCE=" + lua_literal(raw)
    chunk += "\nMOCK_PUBLIC_SOURCES=" + lua_literal(texts)
    chunk += "\nMOCK_MULTI=" + lua_literal(multi)
    chunk += '\ndofile("07_scripts/tracker/tests/cfru_dpe_ui_mock.lua")\n'
    result = subprocess.run([runtime, "-"], input=chunk, text=True, cwd=ROOT, check=False)
    return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
