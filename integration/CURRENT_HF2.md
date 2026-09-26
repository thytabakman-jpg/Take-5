# CURRENT HF2 — Recovery Anchor 001

Date: 2026-09-26
Status: TAKE-5 CANDIDATE / VALIDATION REQUIRED

## Identity

Configured tool:
HF002

User aliases:
HF2
HF-2
HF-002

Runtime:
runtime/hf002_recursive_continuation.py

## Core law

For configured capability C:

C(x_t)
-> normalized x_(t+1)
-> same C(x_(t+1))

only while:

MaterialLocal_t
and Live_C(t+1)
and UpstreamStable_t.

HF2 owns same-capability local recurrence.

It does not own global tool selection or episode terminality.

## Division of labor

HF1:
upstream invalidation / reentry classification.

HF2:
same-capability successor recurrence.

TRC:
consequence closure.

ImprovementCore:
global work selection, admission, cross-capability replanning, terminality.

## Terminal dispositions

RELATIVE_CLOSE
RETURN_REENTER
OPEN
BLOCKED
CONFLICT
RESOURCE_STOP.

RESOURCE_STOP is not semantic completion.

## Anti-loop

Equivalent failed/NoGain routes cannot repeat without invalidating evidence.

## Current use

RootCause is the first Take-5 configured tool explicitly bound to HF2 local recurrence.

RootCause:
runtime/root_cause.py

## Lineage

Recovered from Reaserch:
- HF002_RECURSIVE_CONTINUATION_ENGINE_001_2026-09-26.md
- HF002_FULL_TOOL_MATH_001_2026-09-26.md
- HF002 runtime/ablation evidence.

Take-5 promotion is new and requires Take-5 validation.

## OPEN

- universal wrapper promotion for every Take-5 configured tool;
- minimal generic local state;
- infinite-frontier fairness;
- unbounded termination;
- universal host binding.
