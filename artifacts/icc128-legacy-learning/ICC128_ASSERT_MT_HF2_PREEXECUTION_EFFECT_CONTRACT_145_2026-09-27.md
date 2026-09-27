# ICC128 ASSERT-HF2 / MT-HF2 Loop — Pre-Execution Effect Contract 145

Date: 2026-09-27
Status: IMPLEMENTED ON BRANCH / VALIDATION PENDING
Controller: ICC128 Legacy semantics used as the orchestration model
Branch: fix/preexecution-effect-contract-145

## Reorganized governing prompt

Determine whether the current Specification-Before-Transformation invariant is
actually non-bypassable at every repository-owned point that can change target
reality.

Use the controller loop:

G_Q
-> G_W
-> S
-> E
-> A
-> U
-> G_Q

with repeated local recurrence:

ASSERT + HF2
-> MT + HF2
-> ASSERT + HF2
-> MT + HF2
-> ASSERT + HF2
-> MT + HF2

Reenter only on material discovery/state delta.

Do not equate:
- configured tool execution with target transformation;
- observer analysis with state mutation;
- post-execution admission with pre-execution safety;
- a host-supplied callback with an evidence-only worker unless its effect class is typed.

## Loop result

### ASSERT/HF2 pass 1

Initial evidence suggested three repository bypasses:
- direct formal-tool gateway;
- PTI configured execution;
- ToolConductor factor execution.

Material delta:
shared configured execution did not call the specification gate.

### MT/HF2 pass 1

The first claim contained a category error.

All three routes are governed by the current observer-only configured-tool contract.
Configured analytical execution is not itself a target transformation.

Result:
the alleged three bypasses were not established transformation bypasses.

The relevant object is an authoritative transition, not a tool call.

### ASSERT/HF2 pass 2

Reassertion against current main withdrew the earlier bypass claim.

Confirmed guarded transition surfaces:
- IC-028 selected object-transforming work;
- transform-sensitive strict-progress admission;
- emergent transformation claims;
- Take-6 promotion.

New question:
can a higher-order callback change target reality before those later guards run?

### MT/HF2 pass 2

Factorization exposed two distinct execution species:

1. EVIDENCE_ONLY
   The callback returns evidence/proposals. Target reality is unchanged until a
   later governed admission/update.

2. TARGET_TRANSFORM
   The callback itself can change the target or external reality before return.

Operation class and effect class are independent coordinates.

### ASSERT/HF2 pass 3

Current runtime evidence shows:
- RecursiveImprovementCoreManager invokes run_child before its later strict-progress
  specification check.
- the Legacy candidate invokes generic execute_work before admission/update;
- both callbacks are caller-supplied Python callables;
- neither boundary previously required an execution-effect declaration.

Therefore a mutative callback could act before specification adequacy was checked.

This is a real timing defect.

### MT/HF2 pass 3

Minimal repair:

Let w be a selected work item.

OpLicensed(w)
iff
Recovery(Op(w))
or
(
  Transform(Op(w))
  and SpecAdequate(Object(w),Op(w))
).

EffectLicensed(w)
iff
Effect(w)=EVIDENCE_ONLY
or
(
  Effect(w)=TARGET_TRANSFORM
  and Transform(Op(w))
).

Then

ExecLicensed(w)
iff
OpLicensed(w)
and EffectLicensed(w).

Unknown operation class:
OPEN.

Unknown effect class for a generic/higher-order callback:
OPEN.

Configured repository tool execution may infer EVIDENCE_ONLY because the current
global configured-tool contract is observer-only. It may not infer a missing
operation class for tools whose semantic operation is not intrinsically recovery.

## Implementation

runtime/specification_before_transformation.py
- adds typed execution-effect classes;
- adds ExecutionAdmissionReceipt;
- adds assess_executable_work_item;
- preserves configured-observer inference only for effect class;
- adds MT to the safe recovery-tool operation basis.

runtime/improvement_core_recursive_manager.py
- runs pre-execution admission before run_child;
- untyped or unlicensed child callbacks return OPEN without invocation;
- later strict-progress admission remains a second guard.

runtime/improvement_core_legacy_candidate.py
- leaves the frozen ICC128 Legacy controller unchanged;
- gates modern Legacy formal/generic execution wrappers before callbacks;
- configured observer tools can infer EVIDENCE_ONLY;
- generic higher-order callbacks must declare effect class.

tests/test_preexecution_effect_contract.py
- proves untyped recursive callbacks do not run;
- proves unlicensed target transformations do not run;
- proves adequately specified target transformations can run;
- proves the same behavior for the Legacy higher-order executor.

## Frozen Legacy identity

No file under legacy/icc128-legacy/snapshot is modified.

The historical controller remains:

G_Q -> G_W -> S -> E -> A -> U -> G_Q.

The new rule is a modern wrapper legality condition on what may be supplied to E.

## Current disposition

Implementation delta:
MATERIAL.

Semantic closure:
PENDING CI.

Repository-wide external-host universality:
not claimed.

The next loop pass must run against the validated branch/head. A failed regression
reopens the earliest failed coordinate instead of weakening the invariant.
