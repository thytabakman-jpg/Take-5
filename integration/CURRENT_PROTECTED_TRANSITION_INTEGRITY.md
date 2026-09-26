# CURRENT PROTECTED TRANSITION INTEGRITY — Recovery Anchor 090

Date: 2026-09-26
Status: CURRENT / VALIDATED / MERGED

## Start here

This is the recovery surface for the root diagnosis:

PROTECTED_TRANSITION_INTEGRITY_FAILURE.

Current mathematics:
architecture/PROTECTED_TRANSITION_INTEGRITY_090.md

Core runtime:
runtime/protected_transition_integrity.py

Portfolio audit:
runtime/protected_transition_portfolio.py

Configured execution integration:
runtime/global_tool_execution.py

Generic configured identity:
runtime/configured_run.py
runtime/tool_manifest.py

## Required chain

canonical identity
-> configured dispatch
-> actual execution
-> result consumption
-> state update
-> reentry
-> final user-visible boundary.

A protected behavior is not operationally preserved until every required edge has a witness.

## Recovery commands

Run the tests:

tests/test_protected_transition_integrity.py
tests/test_protected_transition_portfolio.py

Run portfolio audit:

runtime/protected_transition_portfolio.py

## Anti-loss rule

Do not reconstruct PTI as:
- manifest-only identity;
- execution-only receipt;
- response-boundary-only validation;
- Tool Run Closure alone;
- reentry alone.

PTI is specifically the cross-layer chain.

## Relationship to RootCause

RootCause run 089 diagnosed PTI failure as the smallest stable generator for the
current chat recurrence class.

RootCause:
integration/CURRENT_ROOT_CAUSE.md

Validated run:
research/ROOT_CAUSE_RUN_CURRENT_CHAT_089_2026-09-26.md

## OPEN

- universal host interception;
- proof that these seven coordinates are globally minimal;
- automatic witness generation for every external execution environment;
- cross-repository enforcement outside Take-5.


## Validated implementation evidence

PR #69
- merge 73639b7292e0e0d2b876b1751109255038e7f69b
- validation 36222874741
- portfolio audit passed
- end-to-end PTI execution fixture passed
- missing reentry witness fixture failed closed

## Post-repair disposition

Internal Take-5 configured execution:
CLOSED_RELATIVE.

Remaining external residual:
HOST_INTEGRATION_BYPASS.

Executable recheck:
runtime/protected_transition_root_recheck.py
tests/test_protected_transition_root_recheck.py
