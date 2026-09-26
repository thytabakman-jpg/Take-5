# Protected Transition Integrity 090

Date: 2026-09-26
Status: IMPLEMENTED / VALIDATED / MERGED

## Origin

Recovered by validated RootCause run 089.

Root diagnosis:

PROTECTED_TRANSITION_INTEGRITY_FAILURE.

The recurring failure class appeared when a protected behavior existed somewhere but
was not guaranteed across one mandatory, reconstructible, verified transition chain.

## Invariant

For protected behavior b of configured object T, define the transition coordinates:

I(T,b) = <
  canonical_identity,
  configured_dispatch,
  execution,
  result_consumption,
  state_update,
  reentry,
  user_visible_boundary
>.

PTI(T,b)=VERIFIED iff every coordinate is VERIFIED with a non-empty witness.

If any coordinate is OPEN or MISSING:

PTI(T,b)=OPEN.

If any coordinate is BLOCKED:

PTI(T,b)=BLOCKED.

No local success can substitute for a missing downstream coordinate.

## Two levels of enforcement

### Reconstruction integrity

Every configured tool manifest inherits:

PROTECTED_TRANSITION_INTEGRITY.

ConfiguredRunSpec.complete() requires that generic protected behavior.

Therefore a configured tool cannot be mathematically "complete" while omitting PTI.

### Operational integrity

runtime/global_tool_execution.py exposes:

execute_protected_transition(...)

A successful configured execution claim must witness:

identity
-> dispatch
-> execution
-> consumption
-> state update
-> reentry
-> user-visible boundary.

The function does not return a successful configured result until
require_protected_transition(...) passes.

## Portfolio audit

runtime/protected_transition_portfolio.py

For every registered configured tool, the audit verifies:

- ConfiguredRunSpec complete;
- manifest reconstructs PTI;
- full configured execution plan builds;
- formal-object identity reaches the response-boundary registry.

This tests the repair against the entire current configured portfolio, not one tool.

## Root-cause counterfactual

Before this repair, a local mechanism could be fixed while another transition edge
remained unprotected.

After this repair, repository-governed configured execution has one explicit chain
object whose incompleteness is typed and fail-closed.

This is the direct repair predicted by RootCause run 089.

## Runtime

- runtime/protected_transition_integrity.py
- runtime/protected_transition_portfolio.py
- runtime/global_tool_execution.py
- runtime/configured_run.py
- runtime/tool_manifest.py

## Regression

- tests/test_protected_transition_integrity.py
- tests/test_protected_transition_portfolio.py
- tests/test_global_tool_execution.py
- tests/test_configured_run_spec.py

## Boundary

PTI can govern only repository-aware execution that uses the configured Take-5 path.

An unrelated host that never loads Take-5 cannot be compelled by this repository.

Therefore universal host interception remains OPEN.

## Closure rule

This root generator is considered repaired relative to Take-5 repository-governed
configured execution only after:

1. full Take-5 validation succeeds;
2. portfolio audit passes;
3. end-to-end missing-edge fixture fails closed;
4. RootCause/current recovery records are updated;
5. the repair is merged.

The stronger claim "this can never recur in any host" is not licensed.


## Validation evidence

PR #69
Merge: 73639b7292e0e0d2b876b1751109255038e7f69b
Validation run: 36222874741
Conclusion: SUCCESS

The whole configured-tool portfolio inherited PTI, the end-to-end execution gate
returned VERIFIED only with all seven witnesses, and the missing-edge fixture failed closed.

## Post-repair root recheck

runtime/protected_transition_root_recheck.py

After portfolio PTI passes, RootCause no longer treats the internal
PROTECTED_TRANSITION_INTEGRITY_FAILURE as the root of the remaining host-bypass residual.

The surviving residual candidate is HOST_INTEGRATION_BYPASS.

Therefore the internal generator is closed relative to repository-governed configured execution.
