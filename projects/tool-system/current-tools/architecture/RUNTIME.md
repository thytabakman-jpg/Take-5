# Runtime pointer: Architecture

The current Take-5 configured tool ID is `Architecture`. Follow this
execution route without choosing a similarly named historical definition:

1. [Configured-run registry](../../../../runtime/tool_run_registry.py) — exact registered identity `Architecture`.
2. [Current protected manifest](../../../../runtime/tool_manifest.py) — required Architecture behaviours and their executable witnesses.
3. [Portable tool conductor](../../../../runtime/portable_tool_conductor.py) — declares `Architecture`'s native entrypoint, constructs configured-factor execution and requires a caller-supplied adapter where appropriate.
4. [Native architecture analysis](../../../../runtime/architecture_analysis.py) — `run_architecture_analysis(architecture, contract, *, analyze_architecture, protected_constraints=())` enforces the typed output carrier and protected constraints. The `analyze_architecture` function is an **external environment input**, not a built-in universal architecture solver.
5. [Native recovery tests](../../../../tests/test_four_tool_recovery_20260927.py) and [protected unit-job tests](../../../../tests/test_prose_transition_layers.py) — existing evidence for this particular runtime, not proof of external host interception.

The cross-repository Reaserch [GOAL–Architect meta-recursion
contract](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/GOAL_ARCHITECT_META_RECURSION_CONTRACT_001_2026-10-02.yaml)
has a separate hierarchy manager and tool ID. **No binding from the
Take-5 `Architecture` entrypoint to that manager has been established by
this routing page.** Treat that execution-path integration as OPEN until
actual dispatch and same-level pairing tests demonstrate it.

This page records organization and routing only; it does not register an
alias, install an adapter, import other-repository execution authority or
assert that a named tool was run.

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.
