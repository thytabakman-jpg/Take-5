# ImprovementCore Indexed Progress Mathematics 110

Date: 2026-09-26
Status: VALIDATED STRICT-GAIN COMPARISON MATHEMATICS / PROPOSED CURRENT
Base: current Take-5 main
Controller target: ImprovementCore
Primary defect attacked: transition-local progress evidence was being asked to serve as the global strict-improvement relation

## 1. Tool-derived diagnosis

The configured campaign uses:
- ASSERT compound fixed point + full D36_C;
- MT full configured run with synchronous BLACK_BOX_OPEN semantic gate;
- PD;
- PDAudit;
- MTA;
- RootCause under HF2;
- GOAL;
- Architecture;
- Diagnosis;
- MultiObject;
- RTC;
- TRC;
- HF1;
- HF2;
- CurrentnessAudit;
- QuestionWorthAsking;
- SolutionToMyProblem;
- SemanticResolutionPipeline;
- ImprovementCore.

Every configured plan inherits:
- canonical wrapper;
- OBSERVER mode;
- D36_C = Scope x ModeFace;
- Q01-Q22 x 36;
- DIFFERENTIATE / RELATE / RECONSTRUCT / STRENGTHEN x 36;
- recursion;
- closure;
- reentry.

The black-box spine is:

PD
-> PDAudit
-> MTA
-> MT
-> PDAudit
-> C47 Completion Check.

## 2. Root defect

Recovered recurring mathematical failures:

F1
one-step transition evidence was treated as though it already defined a transitive system-level order.

F2
cross-basis comparison was represented by a Boolean "basis reconciled" flag without a mathematical transport witness.

F3
effect labels were used as the definition of gain rather than as evidence for a state-order comparison.

F4
path coherence across basis transitions was OPEN, so transitivity across representation/basis change was not established.

RootCause candidate:

UNTYPED_COMPARISON_RELATION.

The repair is to separate:
1. state comparison;
2. one-step transition certification;
3. recurrence/NoGain memory;
4. closure.

## 3. Basis-indexed state fibers

Let B be the admitted basis family.

For each basis beta define a state fiber:

X_beta.

A state is:

x =
<
P_x,
I_x,
G_x,
V_x,
E_x,
c_x
>_beta

where:

P_x
protected capabilities / protected continuation behavior.

I_x
information state.

G_x
satisfied goal predicates.

V_x
verified reusable contributions.

E_x
execution-truth level.

c_x
burden/cost.

The implementation uses finite witnesses:
- protected_capabilities;
- admissible_models;
- satisfied_goals;
- verified_contributions;
- execution_level;
- burden.

## 4. Information order

Let M_beta(x) be the currently admissible model/hypothesis set.

Within one basis:

x <=_I y
iff
M_beta(y) subseteq M_beta(x).

Thus y is at least as informative as x when it rules out no fewer admissible possibilities.

This order is evidence/authority gated.
An inconsistent empty model set is not automatically counted as improvement.

## 5. Protected semantic preorder

Within a fixed basis beta define:

x <=_beta y

iff all of:

P_x subseteq P_y

M_beta(y) subseteq M_beta(x)

G_x subseteq G_y

V_x subseteq V_y

E_x <= E_y.

Execution truth uses:

NOT_EXECUTED
<
SELECTED
<
BOUND
<
EXECUTED
<
CONSUMED
<
VERIFIED.

Burden is not a hard nonregression coordinate.

Reason:
a genuine semantic improvement can cost more and still be a semantic improvement.

Burden becomes a strict-gain coordinate only inside semantic equivalence.

Define semantic equivalence:

x ~=_beta y

iff
x <=_beta y
and
y <=_beta x.

Then the strict improvement relation is:

x <_beta y

iff

[x <=_beta y
and not(y <=_beta x)]

or

[x ~=_beta y
and c_y < c_x].

This preserves partial ordering instead of forcing one scalar utility.

## 6. Why the previous effect-witness relation was insufficient

A transition-local effect witness can certify:

x --a--> y

but a list of local effects does not automatically provide a transitive order over arbitrary x,y,z.

Therefore distinguish:

StepGain_beta(a,x,y)

from:

x <_beta y.

Effect evidence now supports the coordinate inequalities that establish <_beta.
It does not define <_beta by itself.

This means:

EffectWitness
= proof/evidence object

not

EffectWitness
= order axiom.

## 7. Cross-basis comparison

For beta != gamma, direct comparison is forbidden without transport.

A comparison certificate is:

kappa
=
<
beta,
gamma,
delta,
T_beta->delta,
T_gamma->delta,
Protect,
Authority,
Coherence,
Evidence
>.

delta is a common comparison basis.

The certificate is admissible only when:
- protected semantics are preserved;
- authority is preserved;
- transport is path-coherent;
- evidence is present.

Then:

x <=_kappa y

iff

T_beta->delta(x)
<=_delta
T_gamma->delta(y).

Without kappa:

x and y are INCOMPARABLE / OPEN_COMPARISON.

A Boolean "basis_reconciled = true" is no longer enough.

## 8. Path coherence law

For admitted basis morphisms f and g:

T_id = id

and

T_(g o f)
=
T_g o T_f

on the protected comparison domain.

Where this cannot be established, cross-basis transitivity remains OPEN.

This is the missing path-coherence condition from the earlier mathematics.

## 9. Episode-wide comparison frame

Pairwise certificates are not enough for a long chain when each pair is free to choose a different comparison basis.

For one improvement episode define:

Omega
=
<
omega,
{T_beta->omega}_{beta in B_episode},
Protect,
Authority,
Evidence
>.

Every participating state is transported into the same comparison basis omega.

Then:

x <_Omega y

iff

T_beta->omega(x)
<_omega
T_gamma->omega(y).

This makes the comparison frame itself part of the claim.

A basis missing an admitted transport into Omega is not comparable in that episode.

The finite executable witness is:

ComparisonFrame(
  common_basis=omega,
  transports={beta:T_beta->omega}
).

Because one transport is fixed per participating basis, pairwise frame drift is eliminated inside the episode.

## 10. Transitivity result

Within a fixed basis, <=_beta is a preorder because every coordinate relation is reflexive and transitive.

Its strict part is transitive.

Under admissible path-coherent transport certificates, cross-basis strict comparison composes through a common comparison basis.

Therefore:

x < y
and
y < z

licenses

x < z

only when the comparison transports compose coherently.

The implementation includes a same-basis transitivity regression and cross-basis transport witness.

## 11. One-step transition certification

A transition receipt is:

r =
<
route,
execution truth,
boundary verification,
obligation terminality,
evidence
>.

Classify:

STRICT_GAIN
when
x < y
and execution >= CONSUMED
and the claimed boundary is verified
and obligations are terminal
and evidence exists.

NO_GAIN
when
x ~= y
under the same requirements.

REGRESSION
when
x not<= y.

OPEN_EXECUTION
when execution has not reached the required stage.

OPEN_BOUNDARY
when repository/runtime change has not been verified at the claimed boundary.

OPEN_OBLIGATIONS
when consequence/closure obligations remain.

OPEN_EVIDENCE
when the claimed transition lacks evidence.

OPEN_COMPARISON
when the bases lack an admissible transport certificate.

This directly formalizes:

DOCUMENTED != ACTIVE

SELECTED != EXECUTED

EXECUTED != CONSUMED

REPOSITORY_FIXED != HOST_VISIBLE_FIXED.

## 12. NoGain memory

For a certified no-gain route record:

n =
<
route,
basis,
semantic class,
dependency footprint,
evidence
>.

Retry is blocked while:
- basis is unchanged;
- semantic class is unchanged;
- no changed coordinate intersects the dependency footprint;
- the failure signature remains undefeated;
- no genuinely new interaction package exists.

Thus negative evidence is causally active.

## 13. Semantic cycles

Let q_t be the continuation-equivalence / semantic class of x_t.

A no-gain cycle exists when:

q_t = q_(t-k)

and no strict-gain edge occurs on the intervening path.

Raw artifact IDs, timestamps and file churn do not defeat the cycle test.

The cycle is blocked until a relevant basis/dependency change reopens it.

## 14. Closure

Let L_beta(x) be the live admissible frontier after NoGain blocking and current routing.

RELATIVE_CLOSE requires:

GoalGap(x)=0

L_beta(x)=empty

Coverage_beta = CURRENT

Basis_beta = CURRENT

ProtectedPreservation = PASS

and no OPEN/BLOCKED/CONFLICT obligation remains.

If the goal gap is nonzero and the frontier is empty:
OPEN, not completion.

If coverage or basis changed:
RETURN_REENTER.

If a protected invariant regressed:
REGRESSION.

Resource exhaustion never implies semantic closure.

## 15. Fixed-basis anti-repeat / finite termination bound

Assume:
- fixed basis beta;
- finite semantic quotient Q_beta;
- finite route set R;
- each state-route pair is tested at most once unless dependency evidence changes;
- every executed pair returns STRICT_GAIN, NO_GAIN, or a typed non-success disposition;
- strict gain follows the acyclic strict part of <=_beta.

Then the unchanged fixed-basis execution count is bounded by:

|Q_beta| * |R|.

This is a relative finite-basis theorem.

It is not an open-world termination theorem.

A material basis expansion starts a new comparison episode.

## 16. ImproveCore self-improvement

Let C and C' be current and successor controllers.

C' is admitted as a strict successor only when:
- protected behavior transports and is preserved;
- current historical witnesses remain reachable or are explicitly revised;
- execution identity is current;
- matched regression / holdout evidence exists;
- C < C' for at least one licensed coordinate or C ~= C' with lower burden;
- no protected coordinate regresses.

A controller does not self-certify because it generated its own successor.

Self-application produces evidence.
Admission remains a separate operation.

## 17. Tool algebra

Frontier sum:

A ⊕ B
=
ND(Adm(A union B)).

Interaction product:

A ⊗ B
=
ND(
Adm(
{A o B, B o A}
union
ResidualInteract(A,B)
)
).

The product is generally noncommutative.

Safe division:

A / ~=

means quotient by proved continuation equivalence.

Repeated application:

A^n

is licensed only while each factor produces:
- STRICT_GAIN;
- justified NO_GAIN closure;
- or a typed unresolved state.

An unchanged NO_GAIN factor blocks blind repetition.

## 18. ImproveCore controller consequence

The controller remains set-valued.

The repaired abstract interpretation is:

C*_(J,K)
=
<
X_B,
D,
Gamma,
Adm,
Pi,
T,
Ack,
{<=_beta},
Transport,
Memory,
Tau
>.

Gamma
candidate generation.

Adm
hard legality/admission.

Pi
nondominated policy frontier.

T
raw transition.

Ack
execution / consequence / admission normalization.

{<=_beta}
basis-indexed state preorders.

Transport
cross-basis comparison certificates.

Memory
NoGain / failure / dependency memory.

Tau
basis-relative closure.

No new scalar objective is introduced.

## 19. Validated implementation

Runtime:
runtime/improvement_core_order_math.py

Regression:
tests/test_improvement_core_order_math.py

Coordinator:
runtime/ic123_math_recovery_campaign.py

CI:
.github/workflows/ic123-math-recovery-001.yml

Validation evidence:

- IC123 Math Recovery 001 run 36249306975: SUCCESS
- 61 focused baseline/math regressions: PASS
- ASSERT compound + full36: PASS
- MT synchronous black-box lifecycle: PASS
- RootCause HF2: PASS
- QuestionWorthAsking: PASS
- SolutionToMyProblem: PASS
- ImproveCore math spine: PASS
- configured-tool execution bridge: PASS
- coordinated IC123 campaign: PASS
- campaign artifact 10907903760 uploaded

The campaign also falsified one attempted shortcut: the ImproveCore router correctly preserved a plural nondominated frontier between the indexed-preorder repair and a cheaper effect-label patch. The problem-completion layer, not scalar routing, eliminates the insufficient patch because it does not satisfy the required mathematical effects.

This mathematics is proposed as the current comparison/progress layer while C+ remains the current controller-dynamics abstraction.
