# Current state: GOAL

Projection status: CURRENT
Object status: CURRENT
Species: CURRENT_CONFIGURED_TOOL

## Meaning of CURRENT

The two `CURRENT` fields above identify a **registered current configured-tool
package**, not an independently executed or closed GOAL episode. They do not
establish that MT ran, that GOAL processed candidates, that an external host
used the canonical runtime, or that a parent consumed the result.

The configured Take-5 tool is selected by
[`runtime/tool_manifest.py`](../../../../runtime/tool_manifest.py)
(`manifest_for("GOAL").lineage_contract`) and
[`runtime/portable_tool_conductor.py`](../../../../runtime/portable_tool_conductor.py)
(`compilation_witness("GOAL").entrypoint`).
The current selectors point to the protected
[`GOAL 002 identity`](../../../../architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md)
and the `goal.recover_goal_configured` entrypoint. See
[SOURCE_MAP.md](SOURCE_MAP.md) and [RUNTIME.md](RUNTIME.md).

## Execution and authority boundary

A configured run requires a valid robust-MT preflight receipt, supplied
goal-candidate evidence, and a witnessed configured HF2 path. A missing
or invalid MT receipt leaves native configured GOAL `OPEN` with
`MT_PREREQUISITE_REQUIRED`, even while this package stays `CURRENT`.
The actual resulting status belongs to the run/evidence receipt; no run
is inferred from the package state.

External Reaserch provenance cannot override these configured Take-5
selectors or an independently approved canonical project goal. An unresolved
cross-repository transfer remains `OPEN` at the affected consumer and is
tracked in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

## Projection rule

This file is a disposable current projection over retained authority and
evidence. Live identity/runtime reality remains owned by the shared
registry, manifest and runtime files listed in [SOURCE_MAP.md](SOURCE_MAP.md).
It does not erase history or supersede external semantic authority without
an explicit admitted change.
