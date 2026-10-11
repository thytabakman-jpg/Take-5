# Dependencies: GOAL

## Live configured invocation dependency cone

The configured Take-5 GOAL contract, not file proximity or the latest dated
document, determines this list. Resolve the current selectors through
[SOURCE_MAP.md](SOURCE_MAP.md) and [RUNTIME.md](RUNTIME.md).

- **Registry and tool configuration:** [`runtime/tool_run_registry.py`](../../../../runtime/tool_run_registry.py).
- **Protected specification and behavior selection:** [`runtime/tool_manifest.py`](../../../../runtime/tool_manifest.py).
- **Configured entrypoint selection and conductor:** [`runtime/portable_tool_conductor.py`](../../../../runtime/portable_tool_conductor.py).
- **GOAL native and configured recovery:** [`runtime/goal.py`](../../../../runtime/goal.py), including `recover_goal_configured`.
- **Prerequisite MT semantic-return gate:** [`runtime/mt_semantic_return_gate.py`](../../../../runtime/mt_semantic_return_gate.py). A typed, admitted MT preflight receipt is required; this link is not proof that MT ran.
- **Full configured HF2 execution:** [`runtime/configured_hf2_execution.py`](../../../../runtime/configured_hf2_execution.py) and [`runtime/hf002_recursive_continuation.py`](../../../../runtime/hf002_recursive_continuation.py).

## Evidence and scope boundary

- [`integration/CURRENT_TOOL_REALITY.md`](../../../../integration/CURRENT_TOOL_REALITY.md) records the scope and limits of reported tool-reality audits; it is **not** executable proof.
- [`architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md`](../../../../architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md) is the current manifest-selected mathematical identity; its predecessor remains retained historical lineage, not a competing operational selector.
- Reaserch project-goal authority and GOAL provenance remain separately governed, as documented in [SOURCE_MAP.md](SOURCE_MAP.md); they do not silently override the configured Take-5 invocation.

## Change-impact rule

When one of the live configured dependencies above changes, re-evaluate the
affected configured GOAL consumer, the robust-MT boundary, and the HF2 wrapper
before claiming the GOAL path remains current. A link, manifest entry, code
presence, or unit test is not itself a witnessed full configured execution.
Keep unaffected history and independently owned canonical project goals intact.
