# ImprovementCore Mathematics 086

Date: 2026-09-26
Status: CURRENT STRICT-GAIN MATHEMATICAL CANDIDATE

## Problem

The prior compact controller was:

C_(J,K) = <Z,D,A_(J,K),pi_(J,K),T_(J,K),Tau_(J,K)>.

Later runtime gains added recursive parent/child management and basis-relative learning
memory as an L3 realization layer.

That factorization was operationally useful but mathematically mixed levels:

- recursion changed the admissible action space;
- learning memory changed which actions were admissible;
- both changed the state needed to determine the next policy.

Therefore they belong inside the controller state/transition mathematics rather than
remaining external adornments.

## Augmented controller

Define memory space M as finite route-evidence histories.

A memory record is:

e = <route,basis,disposition,footprint,evidence>.

Define augmented state:

Z^+ = Z x M.

The current controller candidate becomes:

C^+_(J,K)
=
<Z^+,D,A^+_(J,K),pi^+_(J,K),T^+_(J,K),Tau^+_(J,K)>.

## Learning gate

For action a with route id r, basis b and dependency footprint F, define:

Blocked_M(a,b,Delta)
iff
the latest memory record for (r,b) has disposition in
{NO_GAIN, REJECTED, FAILED}
and
Delta intersect F = empty.

A changed coordinate reopens the route exactly when:

Delta intersect F != empty.

## Admissible action space

Let A_base(z) be ordinary admitted controller actions.

Let A_child(z,m) be admissible recursive ImprovementCore child actions.

Then:

A^+(z,m)
=
{a in A_base(z) union A_child(z,m)
 | not Blocked_M(a,b(z),Delta(z))}.

Thus recursive child work is not a new primitive controller.
It is one typed action family inside the same endogenous continuation controller.

## Policy

pi^+_(J,K)(z,m)

selects from A^+(z,m).

The policy therefore depends on both live semantic state and learned route history.

This makes negative evidence causally relevant to future selection rather than merely
stored provenance.

## Transition

For an ordinary action a:

a
-> Execute
-> Admit/Reconcile
-> state delta q
-> memory evidence e'
-> (z',m').

Formally:

T^+((z,m),a)
subseteq
Z^+ + D.

For a recursive child action a_c:

SelectChild(z,m)
-> ChildRun(a_c)
-> ChildReturn r
-> ParentAdmission(r,z,m)
-> ParentUpdate
-> ParentReselection.

The child return itself is not a state transition authority.

## Progress predicate

Define continuation-relevant materiality:

Mat(delta)
iff at least one of:
- material_result_delta
- material_search_delta
- open_refinement
- negative_evidence
- certified_no_gain
- changed_representation.

Then:

Tau^+(z',m') = CONTINUE
and not Mat(delta)
implies
NO_PROGRESS.

A live continuation with no selected admissible action is a typed liveness failure,
not silent completion.

## Memory update

Let L be the learning update.

m' = L(m,a,admission,delta).

Examples:

ADMIT + material delta -> GAIN
NO_GAIN -> NO_GAIN
REJECT -> REJECTED
OPEN -> OPEN.

The next policy is recomputed from (z',m').

## Unified recursion

The current deepest candidate is therefore:

(z_t,m_t)
-> A^+_(J,K)(z_t,m_t)
-> pi^+_(J,K)
-> a_t
-> T^+_(J,K)
-> (z_(t+1),m_(t+1)) or D
-> Tau^+_(J,K)
-> terminate or recompute pi^+.

This absorbs the former L3 recursion/memory layer into L0 controller mathematics.

## Realization mapping

Configured realization still has multiple operational layers:

R0
entry/self-management envelope

R1
observer/inquiry/formalization/work generation

R2
selection/binding/execution/admission/reconciliation/persistence/verification

R3
recursive child realization and learning-memory substrate.

But R3 is now a realization factor of C^+, not a separate mathematical controller layer.

## Strict gain

This change explains two runtime facts that the older C object did not encode:

1. the same semantic state z can yield a different legal next action after NO_GAIN memory;
2. a recursive child run is selected by the same parent policy and does not become
   authoritative merely by returning.

Those are result-sensitive distinctions, so the augmented state is not cosmetic.

## Remaining OPEN

- exact mathematical type of pi^+ when policy selection itself performs search;
- whether memory can be safely quotiented by a sufficient statistic;
- global minimality of Z^+;
- exact upstream zero-request relation generator;
- complete capability-repertoire reachability theorem;
- host-wide enforcement outside a runtime that loads Take-5.

## Current conclusion

The preferred current abstract controller is C^+, not the older C alone.

The older C remains the projection obtained by forgetting learning memory and
recursive-action distinctions.
