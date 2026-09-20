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
| User | Authorizes scope, protected-boundary exceptions, merge decisions, and final acceptance/freeze gates |
| ChatGPT CONTROL | Reads the Project/Issues and canonical repository state, routes the next eligible bounded contract, validates returned revision/evidence, and avoids becoming a second status database |
| Codex | Executes one bounded Issue contract, checks, commits/pushes, and opens/repairs PR evidence on an approved branch; a new Issue/material scope/branch starts a fresh session |
| GitHub Project | Owns operational order, status, priority, and work type |
| Workspace Issue | Owns program-level integration, acceptance, verification, or cross-repo contract |
| PR / checks / evidence | Record the reviewed revision and proof; they are not queue items |
| GitHub repository | Persistent source of truth for branches, commits, pins, merged baseline, and canonical docs |

**CONFIRMED WORKFLOW BOUNDARY:** Repair of the same Issue contract on the same
branch may resume; a new Issue, materially new scope, or new branch starts a
fresh Codex session. Keep one writer per branch.

**INTENDED FUTURE STATE:** Use stronger models or review capacity only where a
future work package documents why the complexity/risk warrants it.
