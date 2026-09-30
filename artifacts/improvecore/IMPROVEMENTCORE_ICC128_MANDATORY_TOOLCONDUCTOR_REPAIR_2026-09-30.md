# ImproveCore + ICC128 Mandatory ToolConductor Repair

Date: 2026-09-30
Status: IMPLEMENTED ON REPAIR BRANCH / VALIDATION PENDING
Branch: fix/controller-tool-conductor-mandatory-consultation-20260930
Math basis: architecture/CONTROLLER_TOOL_CONDUCTOR_MANDATORY_CONSULTATION_005_2026-09-30.md

## Regime identity

This repair promotes current ImprovementCore from regime 091 to regime 092 because mandatory
ToolConductor consultation changes the controller's protected stage semantics. Regime 091
remains the historical default-HF2 promotion point.

## Defect

ToolConductor was real, registered, and executable, but current ImprovementCore and ICC128
did not require it in their normal controller path. Historical all-tools work often used
manually scheduled phases or consumed a prior conductor traversal as evidence.

## Repair

ImprovementCore:
OBJECTIFY -> TOOL_CONDUCTOR -> GENERATE_WORK -> SELECT.

ICC128:
G_Q -> TOOL_CONDUCTOR -> G_W -> S -> E -> A -> U -> G_Q.

Both paths invoke the real ToolConductor product operator over MATERIAL_TOOLS.

## Coverage law

A controller consultation is complete only when every registered tool has exactly one
typed conductor-level disposition in exact registry order.

Individual OPEN/BLOCKED/CONFLICT factors remain evidence. They do not falsely convert a
complete traversal into controller failure.

Incomplete, duplicate, reordered, or untyped coverage fails OPEN.

## Anti-recursion

The active controller adapter is removed before the nested ToolConductor call.

The normal selected-tool adapter map is not automatically forwarded into pre-selection
consultation. Any supplied conductor adapter must be explicitly consultation-safe, preserving
the existing Specification-Before-Transformation gate.

Thus ImprovementCore cannot recursively spawn ImprovementCore through its mandatory
conductor consultation, and ICC128 cannot recursively spawn ICC128.

ToolConductor's existing self-witness remains unchanged.

## Protected behaviors added

ImprovementCore:
IMPROVEMENTCORE_TOOL_CONDUCTOR_PRESELECTION_CONSULTATION

ICC128:
ICC128_TOOL_CONDUCTOR_PREWORK_CONSULTATION

## Runtime witnesses

- runtime/controller_tool_conductor.py
- runtime/ic028_operator.py
- runtime/icc128_autonomous_controller.py
- runtime/tool_run_registry.py
- runtime/tool_manifest.py

## Regression witnesses

- tests/test_controller_tool_conductor.py
- tests/test_improvement_core_manager.py
- tests/test_icc128_current.py

## Legacy boundary

ICC128 Legacy remains immutable and was not modified.

## Scope boundary

This repair integrates ToolConductor into the current controllers.

The separate requested mandatory preflight
ASSERT -> SemanticDeterminacy -> CompressionSafety
remains a distinct next repair and is not silently conflated with this one.

## Closure

Advance to VALIDATED only after Take-5 Validation, Capability Preservation, and the
Tool System Every-Tool Sweep pass on the pull-request head.
