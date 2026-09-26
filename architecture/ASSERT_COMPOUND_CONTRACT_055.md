# ASSERT Compound Contract 055

Date: 2026-09-25

Status: CURRENT WORKING DESIGN AUTHORITY + RUNTIME ORCHESTRATOR IMPLEMENTED

Runtime effect: COMPOUND ORCHESTRATION IMPLEMENTED ON BRANCH; end-to-end semantic stage binding remains OPEN until validation/admission

Purpose: preserve the current full ASSERT tool as a compound discovery engine rather than allowing later conversations to collapse it back into a one-pass assertion scan.

## 1. ASSERT core object

Let Gamma be the accessible evidence state.

The bare assertion operator is:

ASSERT_K(Gamma)
=
{ phi in L | Gamma proves_K phi }

Each proposition may carry one of the epistemic statuses:

TRUE
FALSE
UNKNOWN
CONFLICT

The bare operator is not the normal user-facing ASSERT run.

## 2. Current full ASSERT

Normal ASSERT means the compound fixed-point engine:

ASSERT*
=
Fix[
  ASSERT
  -> COMPARE
  -> RESOLVE
  -> HERE
  -> COMPARE
  -> INQUIRE
  -> REASSERT
]

All components operate under the current wrapper contract rather than as isolated bare calls.

Later stages may revise earlier findings.

## 3. Stage jobs

### ASSERT

Extract propositions licensed by the accessible evidence.

### COMPARE

Compare propositions, objects, representations, versions, and states for equality, difference, dependency, conflict, omission, and supersession.

### RESOLVE

Resolve decidable conflicts and distinctions using available evidence while preserving UNKNOWN, OPEN, BLOCKED, and CONFLICT where resolution is not earned.

### HERE

Recover what is actually present now:
- what exists;
- what is happening;
- what differs;
- what relates;
- what is absent;
- what is unknown.

### COMPARE AGAIN

Recompare after HERE because newly recovered objects or relations can invalidate the first comparison.

### INQUIRE

Generate the questions required to close result-sensitive unknowns, conflicts, omissions, and unsupported transitions.

### REASSERT

Recompute the assertion set after admitted answers and state updates.

## 4. Fixed-point state

Let:

S_n
=
<
  A_n,
  C_n,
  R_n,
  H_n,
  I_n,
  Q_n,
  Z_n
>

where:

A = assertion state
C = comparison state
R = resolution state
H = HERE state
I = inquiry state
Q = live question frontier
Z = admitted world/system state

One round yields:

S_(n+1)
=
ASSERT_Round(S_n)

Answers admitted from inquiry update Z and may change every earlier component.

## 5. Reentry law

Reentry is mandatory when either the world state or discovery state changes materially:

Reenter
iff
Delta_world != 0
OR
Delta_discovery != 0

Delta_discovery includes material changes in:
- representation;
- question frontier;
- candidate universe;
- relations;
- assertion set;
- comparison set;
- unresolved conflict set.

A stable world state is insufficient for closure when discovery is still changing.

## 6. Closure law

ASSERT* closes relatively only when:

Verified
AND ResultStable
AND DiscoveryStable
AND QuestionClosed
AND ResidualClosed

Operationally:

Delta_A
union Delta_C
union Delta_R
union Delta_H
union Delta_I
union Delta_Q
union Delta_discovery
=
empty

and no OPEN/BLOCKED/CONFLICT coordinate remains result-sensitive.

## 7. Wrapper integration

ASSERT* is executed through the canonical wrapper:

Bind
-> Observe
-> Formalize
-> Freeze
-> Goal
-> Focus
-> Architect
-> Route
-> Execute ASSERT*
-> Evaluate
-> Tool Run Closure
-> Update
-> Jane Sync
-> HF1
-> Reobserve

ASSERT* does not replace the wrapper.

The wrapper does not replace ASSERT*.

The logical/kernel legality layer remains prior to ASSERT.

## 8. Geometry and current-use full-36 compatibility

No component receives an untyped bare "36" label.

For normal current-use ASSERT, the operational compatibility default is typed D36_C and all three required surfaces are materialized before the run is considered complete:

ASSERT Layer 1:
- all seven protected ASSERT stages x all 36 D36_C cells.

ASSERT Layer 2:
- all current question families Q01-Q22 x all 36 D36_C cells.

Cognitive 36:
- DIFFERENTIATE, RELATE, RECONSTRUCT, STRENGTHEN x all 36 D36_C cells.

Executable coverage surface:
runtime/assert_full36.py

This fixes current invocation behavior. It does not settle the larger geometry/provenance problem. The exact optimal geometry-selection law and historical Layer 1 / Layer 2 provenance remain OPEN in integration/ASSERT_FULL36_ARCHITECTURE_DEBT_071_2026-09-25.md.

Other admitted geometry types remain:
1
D36_C
D36_H
D216
D288

A different geometry requires explicit authorization rather than silent downgrade.

## 9. Preservation requirement

A future change to ASSERT must preserve or explicitly disposition:
- all seven stages;
- the second COMPARE;
- reassertion;
- inquiry-driven state update;
- world-delta reentry;
- discovery-delta reentry;
- fixed-point stopping;
- UNKNOWN/OPEN/BLOCKED/CONFLICT preservation.

No stage may disappear through compression without a behavioral equivalence proof.

## 10. Current OPEN coordinates

- end-to-end semantic binding of ASSERT/COMPARE/RESOLVE/HERE/INQUIRE/REASSERT stage implementations into the orchestrator;
- exact globally optimal geometry-selection law beyond the current-use mandatory D36_C compatibility default;
- historical provenance and intended semantics of the Layer 1 / Layer 2 split;
- historical provenance and intended nesting of the four cognitive operators;
- exact inquiry cost model;
- exact relationship between ASSERT question frontier and the canonical route trigger ledger;
- regression/holdout witnesses for stage ablation.


## 11. Runtime realization

Executable orchestration surface:

`runtime/assert_compound.py`

Configured-run identity:

`runtime/tool_run_registry.py` registers `ASSERT` as a material strong-claim tool.

Regression surface:

`tests/test_assert_compound.py`

The runtime preserves:
- all seven protected stages;
- the mandatory second COMPARE;
- fixed-point reentry on discovery/world-state change;
- basis-relative closure;
- OPEN return when stabilization is not reached;
- caller-supplied closure gating for result-sensitive OPEN/BLOCKED/CONFLICT obligations.

This implementation establishes the compound orchestration shell. It does not claim that every domain-specific stage implementation or geometry assignment is globally complete.
