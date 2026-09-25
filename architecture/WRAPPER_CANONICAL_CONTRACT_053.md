# Wrapper Canonical Contract 053

Date: 2026-09-25

Status: CURRENT WORKING DESIGN AUTHORITY

Runtime effect: NONE until separately implemented and validated

Purpose: preserve the current wrapper mathematics so future wrapper changes are compared against an explicit artifact rather than reconstructed from chat memory.

## 1. Problem

Wrapper design has been evolving faster than its authoritative state has been externalized.

That creates the recurring failure:

```
improvement
-> implicit rewrite
-> silent loss of a load-bearing part
-> later rediscovery
-> reconstruction
```

The wrapper therefore needs its own preservation contract.

## 2. Wrapper identity

The wrapper is the orchestration object around protected tools, Jane, IC, closure, update, and reentry.

It is not the native tool itself.

It is not the kernel.

It is not the full capability registry.

It is not a synonym for "36".

## 3. Current wrapper spine

The current working design is:

```
B_J
-> O
-> Phi
-> Freeze
-> Goal
-> F
-> A
-> Route
-> Exec
-> Eval
-> C_TR
-> U
-> Sync_J
-> HF1
-> O
```

Compositionally:

```
W[K]
  =
  HF1
  o Sync_J
  o U
  o C_TR
  o Eval
  o Exec
  o Route
  o A
  o F
  o Goal
  o Freeze
  o Phi
  o O
  o B_J
```

HF1 is mandatory. A wrapper without HF1 is a one-pass pipeline, not the current wrapper.

Tool Run Closure remains before persistent update.

Jane synchronization remains after admitted state change and before reentry.

## 4. Stage jobs

### B_J

Bind target, job, identity, authority, and episode constraints.

### O

Observe broadly enough to recover evidence before result-sensitive narrowing.

### Phi

Formalize the observed object mathematically.

### Freeze

Freeze the mathematical object so later machinery cannot silently redefine it.

### Goal

Recover the actual result target for the frozen object.

### F

Recover the result-sensitive focus from the observed and frozen object plus goal.

Exact focus mathematics remains OPEN.

### A

Recover the dependency, ownership, interface, boundary, and execution architecture.

### Route

Deterministically derive required capability families from the mathematical state.

Route replaces unconstrained discretionary "pick the best tool" behavior.

Exact route mathematics remains OPEN.

### Exec

Execute the required native tool package under the selected geometry and authority.

### Eval

Evaluate the result against the frozen mathematical object, goal, obligations, and protected behavior.

### C_TR

Tool Run Closure is the execution-to-admission boundary.

It recursively harvests, dispositions, realizes, verifies, consumes, and preserves OPEN/BLOCKED states.

### U

Apply only admitted consequences to authoritative state.

### Sync_J

Synchronize Jane with the admitted material delta.

### HF1

Route material or result-sensitive deltas to REENTER or REVERIFY.

Reentry returns to observation.

## 5. Geometry is typed, not "36-aware"

The word "36" is overloaded and MUST NOT be used without a type.

Current distinct geometry objects include:

```
D36_C = Scope x ModeFace
D36_H = SourceScope x TargetScope
D216  = SourceScope x TargetScope x ModeFace
D288  = SourceScope x TargetScope x FullMode
```

A stage may be:

```
cell-indexed
geometry-dependent
geometry-validated
scalar
```

Those are not equivalent.

For any operation K:

```
Gamma_K in {1, D36_C, D36_H, D216, D288}
```

The chosen geometry must be explicit.

No stage receives a bare superscript 36 without identifying which geometry and relation are meant.

## 6. Deterministic routing

The system does not ask a free selector which tool "seems useful."

Let x be the frozen mathematical state and Delta(x) its live obligations and defects.

Each tool T_i owns an explicit trigger predicate:

```
Trigger_i(x) in {0,1}
```

Then:

```
P_req(x) = {T_i | Trigger_i(x)=1}
```

Examples:

```
ResultSensitiveDistinction -> PD
UnverifiedPDDistinction -> PD_AUDIT
UnknownFailureGenerator -> ROOT_CAUSE
MultipleInteractingObjects -> MULTI_OBJECT
ArchitectureDelta -> ARCHITECTURE
BasisDelta -> CURRENTNESS
ProtectedBehaviorDelta -> A16 / regression / holdout
ExecutionRealityQuestion -> EXECUTION_TRUTH
ConsequenceConeOpen -> CONSEQUENCE_CLOSURE
```

Unknown trigger mathematics remains OPEN rather than being replaced by intuition.

## 7. Cheap probes and heavy execution

A capability may expose a cheap trigger/probe without performing its expensive analysis.

This permits broad capability availability without mandatory full execution.

```
Probe_i(x)
  -> SELECT
   | NON_APPLICABLE
   | OPEN
   | BLOCKED
```

A cheap probe is not evidence that the heavy tool executed.

Selected is not executed.

Execution truth remains:

```
SELECTED
-> BOUND
-> DISPATCHED
-> STARTED
-> EXECUTED
-> RESULT_CAPTURED
-> CONSUMED
```

## 8. Human-visible mathematics

Visible mathematics is a load-bearing feedback channel, not presentation only.

Let:

```
V_H(W,x) = M_visible
```

and human correction produce:

```
Delta_H
```

Then:

```
ResultSensitive(Delta_H)
  => HF1
  => Observe
  => Phi
```

Examples of valid human corrections include:

- two mathematical objects were conflated;
- a load-bearing term is undefined;
- a stage is in the wrong order;
- an invariant disappeared;
- a geometry was mislabeled;
- two equations claimed equivalent are not equivalent;
- a previously protected behavior vanished.

## 9. Wrapper preservation signature

Every wrapper version W_n has a preservation signature:

```
Psi(W_n)
  =
  <
    ordered_stages,
    stage_jobs,
    invariants,
    geometry_types,
    trigger_contracts,
    authority_boundaries,
    closure_boundary,
    update_boundary,
    sync_boundary,
    reentry_law,
    open_coordinates
  >
```

For any proposed wrapper transition:

```
W_n -> W_(n+1)
```

compute:

```
Delta_Psi = Psi(W_(n+1)) - Psi(W_n)
```

Every material coordinate in Delta_Psi must receive one disposition:

```
PRESERVE
MODIFY_AUTHORIZED
SUPERSEDE_AUTHORIZED
REMOVE_AUTHORIZED
NEW
OPEN
```

No material coordinate may disappear silently.

## 10. Admission law for wrapper changes

A new wrapper version is admissible only when:

```
forall p in Protected(Psi(W_n)):
  Preserved(p,W_(n+1))
  OR AuthorizedChange(p)
```

and:

```
OPEN_result_sensitive = empty
```

and closure/update/reentry invariants remain satisfied.

A local improvement does not self-authorize promotion.

## 11. Mandatory comparison protocol

Before changing the wrapper:

1. Read this artifact.
2. Materialize Psi(W_current).
3. State the proposed delta.
4. Run PD on the delta.
5. Run PD Audit on the distinctions.
6. Run Root Cause when the change repairs a failure.
7. Run Architecture on ownership/order/boundary changes.
8. Run Execution Truth on executable claims.
9. Run A16 / holdout / regression on protected behavior changes.
10. Compute Delta_Psi.
11. Disposition every material coordinate.
12. Update this artifact only after the new design state is explicit.
13. Implement separately.
14. Reverify runtime against this artifact.
15. Reenter through HF1 on any material delta.

## 12. Current protected invariants

The following are protected unless explicitly changed:

```
I1  math before substantive tool execution
I2  observe before result-sensitive narrowing
I3  formalize before goal optimization
I4  freeze before downstream optimization
I5  goal before architecture/tool execution
I6  architecture before execution routing
I7  deterministic trigger/routing preferred over unconstrained chooser behavior
I8  geometry names are typed and non-interchangeable
I9  native tools remain distinct from wrapper machinery
I10 Tool Run Closure precedes persistent update
I11 OPEN/BLOCKED remain typed non-success states
I12 authority cannot expand silently
I13 Jane sync follows admitted material state change
I14 HF1 is mandatory
I15 material/result-sensitive delta triggers REENTER or REVERIFY
I16 reentry returns to observation
I17 visible math may generate result-sensitive human correction
I18 specified != selected != executed != consumed
I19 wrapper changes require Delta_Psi accounting
I20 no protected behavior disappears silently
```

## 13. Current OPEN coordinates

The following remain unresolved and must not be painted as closed:

```
O1 exact Focus mathematics
O2 exact deterministic Route mathematics for every tool
O3 complete trigger equations for the full tool set
O4 exact geometry-selection law
O5 exact Eval mathematics
O6 exact human-visible-math formalization
O7 cost/gain law for cheap probe versus heavy execution where deterministic triggers do not fully settle mode
O8 implementation parity between this design artifact and runtime/math_first_wrapper.py
```

## 14. Relationship to existing artifacts

This artifact complements rather than silently supersedes:

- architecture/KERNEL_MATH_CONTRACT_052.md
- architecture/ARCHITECTURE_DECISION_036_MATH_FIRST_TOOL_SELECTION.md
- architecture/OBSERVER_ALL_TOOLS_SWEEP_038.md
- runtime/math_first_wrapper.py
- runtime/tool_run_closure.py
- runtime/hf_controller.py

Where this working design differs from executable runtime, the difference is OPEN until implementation and verification.

## 15. Stopping rule

Wrapper design work is relatively closed only when:

```
Delta_Psi_result_sensitive = empty
AND
runtime_behavior matches admitted wrapper contract
AND
no live HF1 reentry trigger remains
```

Until then the wrapper remains a versioned working design rather than an implicitly finished object.
