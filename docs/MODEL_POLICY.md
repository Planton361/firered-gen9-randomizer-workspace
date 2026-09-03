# Model policy

**CONFIRMED CURRENT STATE:** The STANDARD adoption profile uses one executing
Codex agent by default. Choose a model by task complexity and risk; a stronger
model is not a habit or a substitute for clear scope and verification.

- Use an independent reviewer only for substantial risk, ambiguous evidence,
  or a consequential design decision.
- Do not construct artificial multi-agent teams for routine work.
- MCP is optional and read-only when explicitly useful; it is not a default
  source of truth.

## Roles

| Role | Responsibility |
|---|---|
| User | Authorizes scope, protected-boundary exceptions, and merge decisions |
| ChatGPT Project Steward | Maintains planning/handoff context from canonical repository files |
| Codex | Executes bounded repository work, checks, commits/pushes, and Draft PRs on an approved branch |
| GitHub | Persistent source of truth for branches, commits, PRs, and merged baseline |

**INTENDED FUTURE STATE:** Use stronger models or review capacity only where a
future work package documents why the complexity/risk warrants it.
