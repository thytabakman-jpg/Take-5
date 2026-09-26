# RootCause Mathematics 087

Date: 2026-09-26
Status: IMPLEMENTED / VALIDATED / MERGED

## Native target

RootCause does not seek merely a causal predecessor.

For protected recurring failure class F and frozen basis K, RootCause seeks the
smallest stable upstream generator g such that:

1. g explains the protected recurrence class;
2. g remains causally relevant across representation changes;
3. removing/repairing g would break the recurrence class under the declared basis;
4. no admitted rival strictly dominates g on those rootness coordinates.

Rootness is therefore claim-relative and recurrence-relative.

## State

Let

R_t =
<F,E,C_t,G_t,X_t,U_t,M_t,K>

where:

F
protected recurring failure class.

E
admitted evidence.

C_t
current causal candidates.

G_t
current causal/upstream relation graph.

X_t
counterexamples and removal tests.

U_t
unresolved rootness obligations.

M_t
failed/equivalent route memory.

K
frozen basis/authority/currentness context.

## Candidate type

A candidate c carries:

<c,
 level(c),
 Explain(c),
 Evidence(c),
 CounterEvidence(c),
 UpstreamOf(c),
 Stable(c),
 BreaksRecurrenceOnRemoval(c),
 Open(c)>.

Levels are descriptive, not a mandatory total order:

SYMPTOM
LOCAL_MECHANISM
ENABLING_CONDITION
OWNERSHIP_CONFIGURATION
REPRESENTATION_TRANSITION
ROOT_GENERATOR.

## Rootness vector

For recurrence class F:

V_F(c) =
<
F subseteq Explain(c),
Stable(c),
BreaksRecurrenceOnRemoval(c),
|UpstreamOf(c)|,
-|CounterEvidence(c)|,
-|Open(c)|
>.

Dominance is componentwise Pareto dominance.

No scalar score is canonical.

The live candidate frontier is the nondominated set.

## Root admissibility

RootAdmissible_F(c)

iff

F subseteq Explain(c)
and Stable(c)
and BreaksRecurrenceOnRemoval(c)
and CounterEvidence(c)=empty
and Open(c)=empty.

A candidate may be causal and still fail root admissibility.

## Smaller-generator challenge

A first-pass root candidate is not locally closed merely because RootAdmissible holds.

The same RootCause capability is reapplied under HF2 to the changed causal state and
attacks the candidate with a smaller-generator challenge.

Local closure requires that no currently admitted rival strictly dominates the candidate
after this reapplication.

## HF2 composition

RootCause local execution is:

RootCause round
-> admitted causal frontier
-> normalized successor
-> TRC
-> HF1 upstream classification
-> HF2 recurrence decision.

When:
- material local causal delta exists;
- RootCause still has a live local discrimination frontier;
- upstream basis remains valid;

HF2 reapplies RootCause to the changed successor.

Thus:

HF2_[RootCause](R_0)
=
R_0 -> Phi_RC -> R_1 -> Phi_RC -> ... -> local disposition.

HF2 owns only same-capability local recurrence.

## ImprovementCore boundary

A local RootCause result returns:

<local_status,root_candidates,rejected,unresolved,trace,parent_handoff>.

ImprovementCore owns:
- admission into global state;
- selecting a different capability after the local episode;
- repairing architecture/system state;
- global reentry and terminality.

Therefore:

RootCause RELATIVE_CLOSE
does not imply
ImprovementCore COMPLETE.

## Local closure

Close_RC,K(R_t)=PASS iff:

1. at least one root-admissible candidate exists;
2. no live smaller-generator challenge remains;
3. every rejected material rival has a discrimination witness;
4. unresolved rootness coordinates are empty;
5. TRC is terminal;
6. upstream basis remains valid;
7. resource exhaustion is not being mislabeled as closure.

Otherwise return OPEN/BLOCKED/CONFLICT/RETURN_REENTER/RESOURCE_STOP as appropriate.

## MT-derived lexical result

The phrase variants:

"Rout Cause"
"Root Cause"
"root-cause"

are spelling/orthographic variants with no protected-result effect.

The load-bearing semantic coordinate is "root".

Changing "root" from:
"smallest stable upstream generator of a recurring failure class"

to:
"any cause"
or
"first cause found"
or
"closest mechanism"
changes the protected result.

Therefore the root criterion is native semantics, not presentation wording.

## Current chat run target

The whole-chat recurrence class includes:

- color contract claimed repaired while output violates it;
- tool exists while normal invocation bypasses it;
- full-run request downgrades to a bare/partial tool;
- migration preserves artifacts while losing behavior;
- recovery material points to stale operating paths;
- host reasoning substitutes for the intended controller.

The validated fixture tests whether the stronger generator

PROTECTED_TRANSITION_INTEGRITY_FAILURE

dominates narrower rivals such as:
FINITE_ALIAS_LIST,
DOCUMENTATION_DRIFT,
ACTIVATION_IDENTITY_LOSS.

## Runtime

runtime/root_cause.py
runtime/root_cause_managed.py
runtime/hf002_recursive_continuation.py

Regression:
tests/test_root_cause_hf2.py

## OPEN

- proof that the rootness vector is globally minimal;
- automated rival generation from arbitrary unstructured corpora;
- automated counterfactual intervention in external systems;
- universal host enforcement;
- infinite-frontier fairness/termination;
- whether a richer causal formalism is needed for cyclic generators.

## Disposition

RootCause is locally executable and HF2-wrapped.

Global promotion requires full Take-5 validation and canonical identity binding.


## Validation evidence

PR #65
Merge: 691462f614dc026ad199f1b343496d06bca4da1e
Validation run: 36222526907
Conclusion: SUCCESS

The chat-derived recurrence fixture executed this mathematics under HF2 and selected
PROTECTED_TRANSITION_INTEGRITY_FAILURE after two local RootCause rounds.
