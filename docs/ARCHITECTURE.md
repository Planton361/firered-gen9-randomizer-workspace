# Architecture

## Integration flow

```text
Workspace policy + pinned source/config
  -> DPE Gen 9 data
  -> CFRU engine integration
  -> private local build
  -> UPR-FVX randomizer output
  -> mGBA smoke evidence
  -> later BizHawk / Ironmon Tracker evidence
```

**CONFIRMED CURRENT STATE:** The workspace coordinates these boundaries but
does not own or embed private runtime artifacts. DPE, CFRU, UPR-FVX, the
Tracker, NatDex references, and other external sources are Git submodules with
repository-pinned Gitlinks. See [.gitmodules](../.gitmodules) and historical
[01_docs/references/tool-manifest.md](../01_docs/references/tool-manifest.md)
for source records.

## Boundaries and integrations

- **DPE -> CFRU:** DPE supplies expanded data; CFRU owns engine integration.
  **CONFIRMED CURRENT STATE.**
- **CFRU -> UPR-FVX:** UPR-FVX reads/writes randomizer-relevant ROM structures;
  CFRU retains runtime ownership. **CONFIRMED CURRENT STATE.**
- **UPR-FVX -> emulator evidence:** Randomizer save/reload evidence is separate
  from emulator boot/runtime evidence. **CONFIRMED CURRENT STATE.**
- **BizHawk / Tracker:** targets for later compatibility work.
  **INTENDED FUTURE STATE.**

## Data and configuration ownership

| Data class | Location / owner | Classification |
|---|---|---|
| Policies, decisions, manifests, sanitized evidence | Workspace Git repository | **CONFIRMED CURRENT STATE** |
| External source revisions | Submodule Gitlinks | **CONFIRMED CURRENT STATE** |
| ROMs, saves, states, generated builds, releases, secrets | Local/private and ignored | **CONFIRMED CURRENT STATE** |
| Broad support profile | Requires completed evidence | **INTENDED FUTURE STATE** |

**CONFLICT:** Historical documents can contain earlier workflow rules or stale
status. They remain evidence but cannot override canonical `docs/` files.
