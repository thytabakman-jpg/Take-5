# MT — Mode, Bias, Delegation, and Interaction Synthesis 002

Date: 2026-09-24
Status: MATHEMATICAL SYNTHESIS CANDIDATE
Authority: research only

## Frozen input

This MT pass takes as input the full current result set concerning:
- Goal-Decoupled Observation Sweep (GDOS);
- focused resolution / contraction;
- the expand-contract and observe-act axes;
- bias perturbation;
- capability combination types;
- Improvement Core tool/skill selection, binding, delegation, execution, and reintegration;
- Kernel placement;
- mode-sensitive capability equivalence.

No downstream experiment is allowed to modify these premises until this MT pass completes.

## 1. Controller-mode space

Let breadth be b in {EXPAND, CONTRACT}.
Let direction be d in {OBSERVE, ACT}.

Mode space:

M0 = EXPAND x OBSERVE
M1 = CONTRACT x OBSERVE
M2 = CONTRACT x ACT
M3 = EXPAND x ACT.

Working interpretations:
M0 = GDOS.
M1 = focused resolution.
M2 = specialized delegated execution.
M3 = broad system intervention / architecture generation.

The four modes are not mutually exhaustive of all possible controllers, but they are the minimal 2x2 factorization supported by current evidence.

## 2. Goal-layer vector

Let goal state be:

G = <g0,g1,g2,g3>

where:
g0 = object identity / freeze;
g1 = observation/discrimination objective;
g2 = intervention/optimization objective;
g3 = system-level research objective.

GDOS approximates:
<1,1,0,1>.

Focused resolution approximates:
<1,1,0_or_local,1> with contracted admissible scope.

Act modes activate g2.

Therefore goal-decoupling is selective coordinate suppression, not absence of goals.

## 3. Endogenous selection pressure

For capability h define structural outcome pressure p(h) as the extent to which h contains an internal selector toward an action, successor, closure, or preferred state before all admissible observations are retained.

Current hypothesis:
Benefit_GDOS(h) tends to increase with p(h).

For low-p(h), precision demand q(h) can dominate and CONTRACT+OBSERVE may provide greater value.

This produces a mode-selection surface rather than one best regime.

## 4. Observation and mutation noncommutation

Let O_i be observer i, U be state mutation, R be reconciliation.

Independent frozen observation:

R({O_i(X0)}_i).

Sequential mutating observation:

O_n(U(...U(O_2(U(O_1(X0))))...)).

Current evidence supports non-equivalence in general.

Thus U is both:
- realization/state transition;
- epistemic intervention.

## 5. Reconciliation object

Candidate reconciliation transform:

Rec : P(Observation) -> ReconciledObservationStructure

with output containing:
- agreements;
- contradictions;
- overlaps;
- dependencies;
- interaction residuals;
- provenance;
- unresolved OPEN;
- confidence/evidence status.

Rec is pre-optimization.
It is not equivalent by definition to RELATE, RECONSTRUCT, ADMIT, or SELECT.

Irreducibility remains OPEN.

## 6. Focused resolution object

Candidate focused resolution transform:

FR(X,q,H)
=
recursive restriction of the admissible unresolved coordinate set
under frozen discriminating question q and capability basis H,
with OPEN/incomparability preserved.

FR differs from goal-directed optimization because it narrows relevance without favoring an intervention outcome.

## 7. Bias perturbation

Given protected semantics P and nuisance coordinate n, choose a perturbation phi_n satisfying:

P(phi_n(X)) = P(X).

Define operational bias residual:

BR(H,X,n,Mode)
=
Out(H,X,Mode) triangle_P Out(H,phi_n(X),Mode).

A material residual identifies nuisance sensitivity, not a psychological diagnosis.

Bias audit requires:
- task-irrelevance witness for n;
- frozen protected result;
- independent execution;
- mode annotation;
- result comparison.

## 8. Interaction algebra

For capabilities a,b define interaction type tau in:

{ADD, SEQUENCE, GATE, ENABLE, INHIBIT, RESIDUAL, MODULATE}.

Interaction object:

I(a,b,X,m,o,tau)

where:
m = controller mode;
o = order.

Material interaction exists when joint behavior changes protected result, OPEN/incomparability, provenance, available continuation, or state transition beyond reconstruction from separate outputs.

Order residual:

OR(a,b|X,m)
=
Out(b∘a,X,m) triangle Out(a∘b,X,m).

Mode residual:

MR(a,b|X,m1,m2)
=
I(a,b,X,m1) triangle I(a,b,X,m2).

## 9. Capability equivalence

Previous contextual equivalence is insufficient.

Candidate:

a ~_{J,Ctx,Mode,N} b

iff a and b reconstruct one another for protected job J across licensed composition context Ctx, controller mode Mode, and relevant nuisance perturbation basis N.

This means quotient classes can split when mode changes.

## 10. Skill-use execution ladder

Define statuses:

CONSIDERED
SELECTED
BOUND
DELEGATED
EXECUTED
RECEIPTED
REINTEGRATED
VERIFIED.

Strict implication is not assumed in reverse.

Real specialized capability use requires at least:

SELECTED ∧ BOUND ∧ DELEGATED ∧ EXECUTED ∧ RECEIPTED ∧ REINTEGRATED.

Current Take-5 repair establishes explicit selection/binding visibility but has not yet generally proved DELEGATED or REINTEGRATED fidelity.

## 11. Delegation bias

A global controller has a structural default path:
internal semantic simulation.

A specialized tool has transition cost:
scope freeze -> bind -> local authority -> execute -> receipt -> reintegrate.

Therefore even an unbiased local selector can exhibit path-dependent preference for semantic simulation because it requires fewer state transitions.

This is an architectural default-path bias.

## 12. Kernel factorization

Kernel K should not choose modes or tools.

Candidate K obligations:
- declared frozen-target integrity;
- declared independent-observer isolation;
- authority legality for local delegation;
- execution-truth distinctions;
- no silent capability bypass;
- provenance/currentness;
- OPEN/incomparability preservation.

Controller R/policy:
- choose mode;
- choose observer/capability;
- choose interaction/package/order;
- decide reentry.

Interface:
- bind and delegate.

Runtime:
- execute.

State:
- store mode, frozen packet, independent observations, receipts, lineage.

Verification:
- compare protected results and perturbation invariance.

## 13. Mode-selection problem

The next irreducible problem is not "which mode is best?"

It is:

Given live state s, target X, protected job J, and failure-risk vector F,
which mode or sequence of modes minimizes relevant information loss while preserving reachability and authority?

Candidate failure-risk coordinates:
- premature pruning;
- irrelevant breadth;
- frame lock;
- omitted variable;
- action paralysis;
- uncontrolled intervention;
- confirmation/anchoring;
- default-path semantic simulation;
- premature closure.

No complete selector is yet justified.

## 14. Minimal experimental predictions

P1 High-p capabilities gain more from M0 GDOS than low-p capabilities.

P2 Low-p precision capabilities gain more from M1 focused resolution than from M0.

P3 Mixed tasks benefit from M0 -> Rec -> M1 more than either mode alone.

P4 Specialized tool invocation succeeds more often under M2 explicit delegation than under broad IC synthesis.

P5 Independent observation before reconciliation preserves more distinct material structure than sequential observation with mutation.

P6 A fixed bias checklist underperforms perturbation-based nuisance sensitivity search on novel nuisance coordinates.

P7 Some capability equivalence classes split across M0/M1/M2.

P8 Canonical Authority should benefit from M1 on proposition/source typing and M0 on corpus/route discovery.

P9 Core System Mathematics should benefit from M0 on primitive-role discovery and M1 on theorem/gap closure.

P10 Kernel should benefit from M0 on responsibility discovery and M1 on exact invariant placement.

## 15. MT disposition

The current evidence supports a larger object:

MODE-SENSITIVE, BIAS-AWARE CAPABILITY ORCHESTRATION

with:
- 2x2 mode space;
- selective goal-coordinate control;
- explicit interaction typing;
- nuisance perturbation;
- delegation ladder;
- mode-sensitive equivalence;
- Kernel-protected experimental integrity.

OPEN:
- complete mode selector;
- reconciliation irreducibility;
- exact pressure metric p(h);
- exact precision metric q(h);
- quantitative information-loss measure;
- optimal interaction sampling;
- runtime validation.
