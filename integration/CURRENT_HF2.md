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

when a material successor is observed, reapply C at least once even if the producer reports the local frontier inactive. Relative closure requires an independently clean successor pass, a valid local closure condition, and no upstream reentry. The live frontier remains relevant to deciding OPEN versus closure after a non-material pass.

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

## Current registered-repertoire promotion

The current finite registered Take-5 repertoire now carries HF2 recurrence as part of the full configured invocation identity.

For current registered tool T:

Rec(T)=HF002

except:

Rec(HF002)=SELF.

Current invocation profile:

FULL_CONFIGURED_HF2_V1.

Protected routes include:
- direct imperative formal-tool commands;
- ImprovementCore selected-tool execution;
- PTI end-to-end configured transitions;
- ToolConductor factor execution.

Recovery anchor:

integration/CURRENT_FULL_TOOL_INVOCATION.md

Whole-repertoire audit:

runtime/full_invocation_portfolio.py

## OPEN

- open-world future or unregistered formal objects until admitted and validated;
- minimal generic local state;
- infinite-frontier fairness;
- unbounded termination;
- universal external-host binding.


## Take-5 promotion evidence

PR #65
- merge 691462f614dc026ad199f1b343496d06bca4da1e
- validation run 36222526907

Promoted validated use:
HF2[RootCause] local same-capability recurrence.

The historical all-tool promotion frontier is now CLOSED_RELATIVE for the current registered Take-5 repertoire. Open-world and external-host universality remain outside that finite claim.


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

Regime-091 promoted use:

HF2[ImprovementCore] is now the default local recurrence layer for ordinary
user-facing ImprovementCore invocation. Reapplication requires both a material-effect witness
and changed semantic state. HF1 upstream reentry escapes the local loop.

Validation surface:
architecture/IMPROVEMENT_CORE_DEFAULT_HF2_118.md

This was the first user-facing default promotion. The later FULL_CONFIGURED_HF2_V1 repair generalized recurrence across the current registered Take-5 repertoire. Open-world and external-host universality remain outside that finite claim.


## ImprovementCore default-promotion evidence

PR #116
- merge: ef2ef2a6fa0c4093c28654f4fda04d68eb4d9869
- Take-5 Validation: 36270165005 SUCCESS
- Capability Preservation: 36270165051 SUCCESS

Promoted validated use:
HF2[ImprovementCore] as default local same-capability recurrence.

Current registered-repertoire HF2 promotion is CLOSED_RELATIVE under FULL_CONFIGURED_HF2_V1. Future unregistered/open-world tools and universal external-host binding remain outside that closure.


## Full configured invocation promotion evidence

Primary profile merge:

PR #117
merge: 2b86fdc500f5ad1b35fa578b7c96bd92feb99f41

Regime-091 transported validation:
- Take-5 Validation 36270850293 SUCCESS
- Capability Preservation 36270850299 SUCCESS

Post-merge bypass closure:

PR #119
merge: f35577993d076e9113db0bc6e62b91d89b062565

Post-merge validation:
- Take-5 Validation 36271301228 SUCCESS
- Capability Preservation 36271301286 SUCCESS

Post-merge Think-big reentry:
tests/test_improvecore_hf2_think_big_reentry_20260926.py

Final repository-owned disposition:

CURRENT_REGISTERED_REPERTOIRE_HF2_INVOCATION = CLOSED_RELATIVE.

Universal external host interception = EXTERNAL_NOT_OWNED.


## Parent-return boundary

HF2 remains a capability-local recurrence operator.

HF2 relative closure does not authorize a user-visible ImprovementCore return.

For user-facing ImprovementCore, the current composition is:

HF2[ImprovementCore]
-> ParentReturnGate
-> {
     RETURN,
     CONTINUE -> HF2[ImprovementCore]
   }.

The parent gate is:
runtime/improvement_core_return_gate.py

Canonical architecture:
architecture/IMPROVEMENT_CORE_PARENT_RETURN_CLOSURE_139.md

Therefore repeated user prompts are not the intended outer recurrence mechanism. When repository-owned work remains, the parent gate returns CONTINUE internally and the complete ImprovementCore+HF2 path executes again before a user-visible return.
