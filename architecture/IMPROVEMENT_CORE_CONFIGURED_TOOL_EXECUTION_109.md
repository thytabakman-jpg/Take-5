# ImprovementCore Configured Tool Execution Bridge 109

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE
Parent: integration/CURRENT_IMPROVEMENT_CORE.md
Target regime: 089

## Defect

ImprovementCore had a powerful configured-tool repertoire and a complete global
D36_C execution-plan builder, but the parent controller did not require selected
formal tools to cross into those runtimes.

The live path was:

SELECT
-> generic BIND callback
-> generic EXECUTE callback.

Therefore a handler could name MT, PD, RootCause, ASSERT, GOAL, Architecture, or
another registered tool while EXECUTE still consisted only of host-authored
analysis.

This is the concrete recurrence behind the user's report that ImproveCore was
not using its tools.

## Category error in the prior audit

The previous repertoire reachability audit established:

registered identity
+ reconstructible manifest
+ complete D36_C execution plan.

That establishes configured plan reachability.

It does not establish:

selected formal tool
-> adapter invocation
-> native result
-> controller-state consumption.

The old closure language therefore overstated execution reachability.

## Repair

New runtime:

runtime/improvement_core_tool_bridge.py

The IC-028 BIND/EXECUTE path now enforces:

selected registered formal tool
-> canonical tool identity
-> CONFIGURED_RUNS lookup
-> full build_tool_execution_plan
-> bound configured adapter
-> adapter invocation
-> execution receipt
-> result consumption into controller state.

A missing adapter returns:

OPEN
CONFIGURED_TOOL_ADAPTER_REQUIRED:<tool>

It cannot silently fall back to generic EXECUTE reasoning.

Multiple tools execute only when SELECT explicitly supplies an ordered
selected_tools sequence. The bridge does not infer a tool-smash sequence from
mere salience.

## Full configured binding

Every selected tool receives its current ConfiguredRunSpec and the global
configured execution plan.

The current plan preserves:
- wrapper required;
- observer mode;
- D36_C;
- 36 cells;
- declared native layers over all cells;
- Q01-Q22 over all cells;
- DIFFERENTIATE / RELATE / RECONSTRUCT / STRENGTHEN over all cells;
- recursion / closure / reentry requirements inherited from the configured spec.

The bridge does not claim that constructing the plan alone executes native
semantics. Native execution is represented by the required bound adapter call.

## Controller integration

runtime/ic028_operator.py now:
- binds explicit selected formal tools after BIND;
- invokes bound adapters before the ordinary EXECUTE handler;
- writes CONFIGURED_TOOL_BIND and CONFIGURED_TOOL_EXECUTE receipts;
- consumes tool outputs into configured_tool_outputs;
- stops OPEN/BLOCKED/CONFLICT before generic EXECUTE can impersonate success.

The adapter map is threaded through:
- runtime/improvement_core_dispatch.py
- runtime/improvement_core_regime.py
- runtime/improvement_core_manager.py
- runtime/ic028_operator.py.

## Repertoire audit correction

runtime/repertoire_reachability.py now separately checks:
- current identity;
- protected-transition/plan reconstruction;
- actual controller bridge invocation.

For every configured tool, the bridge audit binds the full plan, invokes a
synthetic witness adapter, and verifies result consumption. This proves
controller-to-adapter reachability under the current repository basis.

It does not claim a native semantic adapter exists for every historical tool.

## Self-study activation

runtime/improvement_core_self_study.py no longer demonstrates a tool-blind
SELECT/BIND/EXECUTE episode.

The current self-study explicitly selects and executes:
- CurrentnessAudit;
- RootCause;
- QuestionWorthAsking;
- ASSERT.

Each receives a full D36_C configured plan and calls its native runtime.
The workflow fails when those execution receipts are absent or lose the 36-cell
binding.

## Protected behavior

SELECTED_FORMAL_TOOL_REQUIRES_CONFIGURED_NATIVE_EXECUTION

MISSING_SELECTED_TOOL_ADAPTER_PRESERVES_OPEN

CONFIGURED_TOOL_RESULT_IS_CONSUMED_BEFORE_GENERIC_EXECUTE

PLAN_REACHABILITY_IS_NOT_EXECUTION_REACHABILITY

## Remaining boundary

Repository code cannot synthesize host capabilities that are not bound.

For a selected tool whose native adapter is unavailable in the active host,
the legal disposition is OPEN with the missing-adapter identity.

Universal external-host interception remains EXTERNAL_NOT_OWNED.
