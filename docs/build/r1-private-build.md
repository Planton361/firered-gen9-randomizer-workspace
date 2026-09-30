# R1 private build

The canonical private artifact flow is:

```text
04_private_roms/<input>.gba
          ↓
       runner
          ↓
05_builds/test.gba
```

This user-owned POSIX command builds Clean FireRed → DPE → CFRU using exact
committed source exports. Run it from the Workspace checkout containing the
runner:

```sh
python3 07_scripts/build/run_r1_private_build.py \
  --base-rom "/workspace/04_private_roms/FireRed private input.gba" \
  --output /workspace/05_builds/test.gba
```

The example path is a placeholder. The input may have any filename, including
spaces; the runner copies it into its disposable DPE tree as `BPRE0.gba`. The
input and output may live in a different local Workspace checkout than the one
containing the runner. That storage checkout may be dirty or on an older branch:
the runner reads only the private input there and publishes only the final
output there. It does not use that checkout as a build source, change its
Gitlinks or branch, or run Git write commands there.

Artifact paths are accepted only after canonical path resolution proves they
are below that checkout's `04_private_roms/` or `05_builds/` directory and Git
reports both the zone and target path as ignored. Symlink inputs are rejected;
symlinked zones or parent paths that resolve outside the approved zone are
rejected. An outside alias is accepted only when its resolved path proves the
same canonical ignored zone. The output parent must already exist. An existing
output is preserved and causes failure; there is no overwrite option.

`--output /workspace/05_builds` is a directory shorthand for
`/workspace/05_builds/test.gba`, but only when the argument resolves to that
existing canonical ignored build directory. The runner never writes the
persistent final ROM to `02_external/CFRU-expansion/test.gba`.

Private paths stay local; the runner neither analyzes ROM contents nor requires
a ROM hash. It does not upload artifacts or perform Git writes. Routine status,
CLI errors, and child-process failures do not echo private paths. Child output
is suppressed and no build logs are retained.

Initialize the three registered component submodules at their Workspace pins
before running. Python 3, Git and these PATH tools are required:
`arm-none-eabi-as`, `arm-none-eabi-gcc`, `arm-none-eabi-ld`,
`arm-none-eabi-objcopy`, `arm-none-eabi-objdump`, `arm-none-eabi-nm`,
`grit`, `wav2agb`, `mid2agb`. Missing tools are reported by name only;
nothing is installed. Windows is unsupported by this runner.

Supported profile:

| Source | Exact revision |
| --- | --- |
| Workspace integration base | `5a14e200c926646886990d0a802ffe878dcaf9f5` |
| CFRU | `c9a7f19f1e8aaebd33213503f32fa7bba59ce81c` |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX (reference only, not built) | `7bf79ee1e7c46c972f7a9c84942970a950be0723` |

Workspace descendants are supported only when their diff from the integration
base is confined to this runner, its focused test file, and this usage document.
HEAD Gitlinks, index Gitlinks and component HEADs must match. Local component
file edits are never consumed: only the exact committed trees are exported.
Source export uses `git archive` with a fixed set of Git-side excludes, so
command size does not grow with repository file count. Top-level `deps/`,
`build/`, `.git/`, ROM/save/state files, executable/archive extensions and
`.env*` entries are excluded before the archive stream is produced.
Pre-tooling ROM product-source provenance remains
`b20454789e375383eb852d749c0357d58af461dc`.

The output parent must already exist. Input must be a regular file outside the
Workspace; symlink inputs are rejected. Output and temporary build storage must
be outside Git checkouts. Existing destinations, including dangling symlinks,
are rejected; there is no overwrite option. Publication uses an atomic,
no-overwrite hard link within the destination filesystem. A filesystem that
cannot support this operation fails safely.

Profile/toolchain validation and DPE source build precede private input copying.
The pipeline runs DPE `scripts/build.py`, DPE `scripts/make.py`, CFRU
`scripts/build.py`, then CFRU `scripts/make.py`. Both `make.py` scripts perform
their own additional build internally. The DPE make invocation uses a small
in-process checked `os.system` adapter because this exact legacy pin otherwise
ignores its inserter's exit status. Exported source files and registered
checkouts are not edited by the adapter. CFRU's pinned inserter already runs its
source-contract and linked AI preflights; the runner adds no full acceptance
suite. DPE has no standalone source/module test gate at this pin.

Each insertion requires absence of `test.gba` immediately before invocation,
exit 0, and a regular, non-symlink output afterward. Isolated trees establish
freshness without ROM analysis. DPE's `test.gba` is handed to CFRU as
`BPRE0.gba`; CFRU still creates its own internal `test.gba` only inside the
disposable build tree. The final persistent `test.gba` is copied to
`05_builds/test.gba` only after both insertions succeed and temporary cleanup
completes. A later step never runs after a failed stage. Temporary source trees
and private intermediate outputs are removed on success, failure and handled
interruption. The final output is staged locally, the build area is cleaned,
and only then is the destination published. If cleanup cannot complete, the
runner reports failure rather than READY. OS/filesystem failures that prevent
removal require local user attention; abrupt kill/power loss cannot run Python
cleanup.

CLI exit codes:

- `0`: all stages, publication and cleanup succeeded; `Final output: READY`.
- `1`: profile/toolchain/export/build/insert/input/output/cleanup failure or
  handled KeyboardInterrupt; sanitized stage/reason under
  `R1_PRIVATE_BUILD_FAILED`.
- `2`: invalid CLI arguments; sanitized CLI failure.

Run the ROM-free synthetic suite with:

```sh
python3 07_scripts/build/tests/test_r1_private_build.py
```

This orchestration evidence is not a private build or runtime PASS.
`ROM_PROFILE_READY` remains not accepted; the user-owned private build and
revision-bound R1 runtime acceptance remain downstream of integration.
