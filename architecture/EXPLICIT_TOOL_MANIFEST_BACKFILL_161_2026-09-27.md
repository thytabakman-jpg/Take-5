# Explicit Tool Manifest Backfill 161

Date: 2026-09-27
Status: VALIDATED ON PR #161 HEAD 02fa863b

## Problem

The configured repertoire and native execution portfolio had become substantially
stronger than the explicit tool-specific manifest layer.

That created a misleading residual: many tools with executable typed identities
were classified as generic-only even though their identity contracts already
existed in authoritative registries or dedicated runtime modules.

## Admission rule

Backfill an explicit manifest only when the identity can be projected from an
existing executable typed source.

Do not create an explicit manifest merely to make the audit green.

## Registry-defined capabilities

C01 through C49 derive their explicit identity from:

- runtime/a5_programs.py;
- runtime/capability_runtime.py;
- tests/test_a5_registry.py;
- tests/test_all_capabilities_execute.py.

Each manifest projects the registered job and protected outputs. No new C-tool
semantics are introduced.

## Learning tools

The admitted learning-tool identities derive from:

- runtime/learning_tool_bridge.py;
- runtime/learning_operator_tools.py;
- tests/test_learning_tool_configured_runs.py.

Each explicit manifest projects the existing typed obligation, input type, and
output type.

## Dedicated native identities

The following registered tools already have dedicated native runtime modules and
are backfilled explicitly from those modules:

- Reconciler;
- DelegatedExecutor;
- TRC;
- CurrentnessAudit;
- CapabilityFoundry;
- EmergentAdmission;
- HistoricalReconstruction;
- ZeroRequest;
- SolutionToMyProblem;
- DesiredJane;
- QuestionWorthAsking;
- LambdaMath;
- SemanticResolutionPipeline;
- ToolConductor.

## Deliberate residual

No explicit identity is synthesized here for:

- MTA;
- Architecture;
- PD;
- PDAudit.

The stale PR #137 contains candidate implementations for these names and passed
its historical branch validation. However, the exact candidate formulas used by
that branch are not independently present as current canonical defining artifacts.
They remain recovery evidence rather than authority.

## Target state

After validation, the explicit-manifest residual and native-runtime residual are
the same exact four-element set:

MTA, Architecture, PD, PDAudit.

This alignment makes the remaining strong tool-reality frontier precise.


## Validation

PR #161 head `02fa863b9de5abeba786ecce63c66167c32fb91a` passed:

- Take-5 Validation run 36302187179;
- Capability Preservation run 36302187186.

The validated residual at the explicit-manifest layer is exactly:

- MTA;
- Architecture;
- PD;
- PDAudit.

The same four identities remain the native-runtime residual.
