# Runtime pointer: GOAL

## Configured execution path

The configured Take-5 GOAL entrypoint is **`goal.recover_goal_configured`**
in [`runtime/goal.py`](../../../../runtime/goal.py), as selected by
[`compilation_witness("GOAL").entrypoint`](../../../../runtime/portable_tool_conductor.py).
The configured call requires both `goal_candidates` and a valid
`goal_mt_receipt` for the robust-MT black-box semantic-return preflight.
Missing or invalid MT evidence returns `OPEN` with
`MT_PREREQUISITE_REQUIRED`; it does not silently fall back to a bare GOAL call.

Live configuration/authority comes from
[`runtime/tool_run_registry.py`](../../../../runtime/tool_run_registry.py),
[`runtime/tool_manifest.py`](../../../../runtime/tool_manifest.py) and the
[GOAL source map](SOURCE_MAP.md), not from this organizational pointer.
Use `manifest_for("GOAL").lineage_contract` to resolve the current protected
mathematical specification; do not choose an older dated specification or
cross-repository provenance link as a substitute.

## Native operator (not configured-run proof)

`goal.recover_goal` in [`runtime/goal.py`](../../../../runtime/goal.py)
is the underlying deterministic recovery operator over *supplied* goal candidates.
It is useful for native unit tests, but a successful call to that function alone
does **not** establish that the configured tool or its robust-MT prerequisite ran.
Candidate extraction from arbitrary prose remains an external semantic input,
not a capability of this pointer, the native core or the manifest.

Execution orchestration remains owned by
[`runtime/portable_tool_conductor.py`](../../../../runtime/portable_tool_conductor.py).
This package records organization and source routing only.

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint,
executed run, consumed receipt and parent closure remain distinct objects.
If the configured witness, manifest, source map and this pointer disagree,
record `OPEN`, repair the active owner/consumer path and verify before asserting
a configured GOAL execution.
