# Reproducibility

## Revision-specific evidence

**CONFIRMED CURRENT STATE:** Evidence applies only to the documented workspace
commit, submodule Gitlinks, configuration, and declared test scope. A later
upstream revision or local artifact is not covered automatically.

Current baseline Gitlinks are repository evidence, including CFRU
`8e3fa8378d67dfe4011d6994469c3806f32764c4`, DPE
`22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`, UPR-FVX
`1a597a667129b50284dd88afb231372b5bd01d7f`, Ironmon Tracker
`c450ecaee2d8131a2789bb656e3be792a93712fb`, and NatDexExtension
`a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.

## Evidence levels

1. Source/static analysis
2. Syntax/structural check
3. Build or randomizer load/save/reload evidence
4. Emulator boot and targeted runtime smoke
5. Broad playthrough, target-emulator, and support-profile evidence

**CONFIRMED CURRENT STATE:** Build, randomizer, and runtime evidence are
separate. Do not promote a feature or support claim beyond completed evidence.

## Protected artifacts

ROMs, saves, emulator states, builds, tool releases, private paths, and
secrets are local/private artifacts. They may support a local test but must not
enter Git, prompts, or agent context. Sanitized evidence records the revision,
scope, method, result, caveats, and next required level without exposing them.

**UNKNOWN:** A stable support profile is not established until all required
evidence for its explicitly defined scope is completed.
