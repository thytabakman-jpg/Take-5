# CURRENT HF2 — Recovery Anchor 001

Date: 2026-09-26
Status: TAKE-5 CURRENT / VALIDATED FOR PROMOTED USE

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


## Take-5 promotion evidence

PR #65
- merge 691462f614dc026ad199f1b343496d06bca4da1e
- validation run 36222526907

Promoted validated use:
HF2[RootCause] local same-capability recurrence.

Universal HF2 wrapper promotion across every configured Take-5 tool remains OPEN.


## ImprovementCore campaign composition

Validated explicit campaign composition:

HF2[ImprovementCore]_campaign

Evidence:
- artifacts/improvecore/IMPROVEMENTCORE_HF2_OBSERVER_CAMPAIGN_115_2026-09-26.md
- artifacts/improvecore/IMPROVEMENTCORE_HF2_THINK_BIG_SELECTION_116_2026-09-26.md
- artifacts/improvecore/IMPROVEMENTCORE_HF2_THINK_BIG_FIX_CLOSURE_117_2026-09-26.md

Observed behavior:
- observer pass reapplied the same ImprovementCore capability twice on material/local/live deltas and then RELATIVE_CLOSE;
- action pass with command "Think big, fix this." reapplied ImprovementCore once after execution-truth strengthening and then RELATIVE_CLOSE;
- PTI remained preserved;
- universal host interception remained EXTERNAL_NOT_OWNED.

This validates the explicit campaign composition.

It does not promote HF2 as a universal wrapper for all ImprovementCore invocations.

Universal HF2 wrapper promotion remains OPEN.
