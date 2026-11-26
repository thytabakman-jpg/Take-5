# Tool Execution Guide

## Purpose and authority

Use this guide to invoke current registered Take-5 tools through their full configured execution path.

The [invocation architecture](../architecture/Tool%20Execution%20Architecture.md) governs the formal requirements. The [live registry](../runtime/tool_run_registry.py), [manifest](../runtime/tool_manifest.py) and runtime govern exact executable identities and behaviour. Resolve discrepancies against those authorities; preserve unresolved discrepancies as OPEN.

For a ChatGPT Python environment, follow the [runtime bootstrap instructions](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/README.md) to load and verify the current main revision before invoking tools.

## Configured execution requirements

Use the registered `ConfiguredRunSpec` and `FULL_CONFIGURED_HF2_V1` profile. [ConfiguredRunSpec.complete()](../runtime/configured_run.py) must pass, including wrapper, OBSERVER mode, D36_C, closure, reentry, OPEN preservation, protected transition integrity and recurrence requirements. Manifest reconstruction includes `CONFIGURED_HF2_RECURRENCE` and `FULL_CONFIGURED_INVOCATION_PROFILE`.

Construct the plan with [build_tool_execution_plan](../runtime/tool_execution_plan.py). Require exact, unique coverage of the 36 cells, every registered native layer across those cells, Q01–Q22 (792 projections), and DIFFERENTIATE, RELATE, RECONSTRUCT and STRENGTHEN (144 projections). Counts alone do not establish completeness.

## Execution routes

| Request | Entrypoint |
| --- | --- |
| Direct tool command | [direct_tool_command_gateway.py](../runtime/direct_tool_command_gateway.py): `execute_direct_tool_commands` |
| ImprovementCore-selected tools | [improvement_core_tool_bridge.py](../runtime/improvement_core_tool_bridge.py): `bind_selected_tools`, `execute_bound_tools` |
| Protected transition | [global_tool_execution.py](../runtime/global_tool_execution.py): `execute_protected_transition` |
| ToolConductor factors | [portable_tool_conductor.py](../runtime/portable_tool_conductor.py): `run_tool_conductor` |

The routes share the configured plan and [recurrence executor](../runtime/configured_hf2_execution.py), `execute_configured_with_hf2`, subject to their explicit self-execution exceptions. Consume its `ConfiguredHF2ExecutionResult` projections for the configured disposition, admitted material change and recurrence receipt; route-specific authorization and result consumption remain with their respective owners. Do not substitute a one-shot native function call.

For direct commands, establish the actual authorized request before submitting it. Prefer an ordered list or tuple of exact registered IDs, for example `("MT", "GOAL")`. Empty batches, duplicate IDs, non-string entries and unregistered IDs are rejected. Verify that the ordered bound identities match the authorized request; inherited selections cannot add tools. The legacy imperative string interface also accepts registered commands (for example, `run MT`); recognized unregistered formal commands fail closed, including mixed requests. Neither interface determines natural-language authorization.

## Recurrence and termination

Read the recurrence engine from the configured identity and plan. Ordinary tools use HF002; HF002 itself uses SELF without a second outer HF002.

When upstream control permits continuation, reapply the same capability after each material local successor, even if its live-local frontier is inactive. Relative closure requires a subsequent non-material pass, no unresolved affected-scope obligations, no live frontier and a satisfied local-close condition. Preserve upstream reentry, OPEN, BLOCKED, CONFLICT and resource exhaustion as distinct dispositions.

## Execution integrity

Bind a task-appropriate adapter and supply the admitted semantic inputs, evidence and authority required by the [worker adapter contract](../architecture/Semantic%20Worker%20Contract.md). A missing adapter or material input remains OPEN. Invalid configured identity or recurrence blocks execution.

Retain the actual native result, execution truth, provenance, coverage, recurrence receipt and unresolved obligations. Distinguish IMPLEMENTATION_EXECUTED, SEMANTICALLY_APPLIED and FULL_MATCH. A complete plan, native function call, routing check or host analysis alone is not evidence of full configured semantic coverage. Do not substitute host prose for a missing native execution or authorize a mutation from a tool receipt alone.

These requirements govern Take-5-owned execution routes, not unrelated external hosts. Unregistered or future formal objects are not implicitly covered.
