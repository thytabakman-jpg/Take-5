# Global Tool Execution Contract 072

Date: 2026-09-25

Status: GLOBAL REPAIR CANDIDATE

## Problem

Tool execution semantics were richer in wrapper/design artifacts than in the configured-run registry. ASSERT received a special full-36 repair, while other registered tools could still satisfy ConfiguredRunSpec without wrapper, geometry, question-layer, cognitive-layer, or observer-default guarantees.

The user also had to explicitly request observer mode. That is itself a defect. Analytical and diagnostic tool runs must not depend on the user remembering to restate a control invariant.

## Governing rule

For every registered tool T:

RunProfile(T)
=
<
  wrapper_required,
  OBSERVER,
  D36_C,
  NativeLayers(T),
  Q01..Q22,
  {DIFFERENTIATE,RELATE,RECONSTRUCT,STRENGTHEN},
  recursive,
  closure,
  reentry,
  OPEN-preservation
>

A configured tool run is complete only when all coordinates are present.

## Coverage

Let C_36 be the 36 cells of Scope x ModeFace.

For every registered tool T:

NativeCoverage(T)
=
NativeLayers(T) x C_36

QuestionCoverage(T)
=
{Q01,...,Q22} x C_36

CognitiveCoverage(T)
=
{DIFFERENTIATE,RELATE,RECONSTRUCT,STRENGTHEN} x C_36

Normal tool entry requires all three.

ASSERT preserves its two declared native layers:
ASSERT_LAYER_1 and ASSERT_LAYER_2.

Other tools declare at least one native layer, defaulting to their exact registered tool identity.

## Observer law

Normal registered tool invocation is OBSERVER only.

A request to run a tool in a non-observer mode is rejected at the global execution-plan boundary.

State mutation is not another tool mode. Mutation occurs only through a separate authorized transition, admission, and commit path.

Therefore the user does not need to remember to say observer mode.

## Runtime

- runtime/configured_run.py
- runtime/tool_run_registry.py
- runtime/global_tool_execution.py

## Validation

tests/test_global_tool_execution.py verifies every registered material tool, not a curated subset.

## Host boundary

Repository enforcement cannot force an unrelated host or chat surface that bypasses the repository entirely. Any host integration claiming Take-5 configured-tool execution must bind through this contract or remain OPEN/BLOCKED as an integration defect.
