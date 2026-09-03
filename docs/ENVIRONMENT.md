# Environment

## Canonical baseline

**CONFIRMED CURRENT STATE:** Linux/CachyOS is the canonical development
environment and POSIX-compatible commands are the default. PowerShell material
is **LEGACY / OPTIONAL COMPATIBILITY GUIDANCE**, retained for historical
Windows workflows only.

| Requirement | Role | Classification |
|---|---|---|
| Git with submodules | Pinned source checkout | **CONFIRMED CURRENT STATE** |
| Python 3 | Bootstrap and safety helpers | **CONFIRMED CURRENT STATE** |
| Java / Gradle | UPR-FVX source work | **CONFIRMED CURRENT STATE** |
| devkitPro / devkitARM and GNU Make | DPE/CFRU build tooling | **CONFIRMED CURRENT STATE** |
| mGBA | Current targeted smoke emulator | **CONFIRMED CURRENT STATE** |
| BizHawk / Ironmon Tracker | Later validation targets | **INTENDED FUTURE STATE** |

## Version policy

Use an exact version only when repository evidence records it for the relevant
revision. Submodule Gitlinks are the authoritative source revision for a
checkout; historical source/version evidence is retained in
[01_docs/references/tool-manifest.md](../01_docs/references/tool-manifest.md).

**UNKNOWN:** No canonical host-package version inventory is established by
M-000R. Do not invent Python, Java, Gradle, devkitPro, GNU Make, or emulator
versions in task reports.

## Safety command

Run from the workspace root before changes and before handoff:

```sh
python3 07_scripts/bootstrap/check_git_safety.py
```

For read-only/bootstrap inspection on `main`, use the explicit exception:

```sh
python3 07_scripts/bootstrap/check_git_safety.py --allow-main
```
