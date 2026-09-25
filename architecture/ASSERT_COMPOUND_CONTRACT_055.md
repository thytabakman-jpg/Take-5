# ASSERT Compound Contract 055

Date: 2026-09-25

Status: CURRENT WORKING DESIGN AUTHORITY

Runtime effect: NONE until separately implemented and validated

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

## 8. Geometry

No component receives an untyped bare "36" label.

Each ASSERT component may use an explicit geometry chosen from the currently admitted geometry family:

1
D36_C
D36_H
D216
D288

or a later admitted geometry.

Geometry is selected by typed applicability, not by naming convention.

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

- exact executable runtime binding for ASSERT*;
- exact geometry assignment for each stage;
- exact inquiry cost model;
- exact relationship between ASSERT question frontier and the canonical route trigger ledger;
- regression/holdout witnesses for stage ablation.
