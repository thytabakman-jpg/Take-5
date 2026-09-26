# ImprovementCore Canonical Progress Mathematics 001

Date: 2026-09-26
Status: PROMOTED CURRENT / REGIME 090
Canonical comparison base: Take-5 regime 089
Evidence basis: current Take-5 math spine, recovered Reaserch lineage, ZIP-study evidence, four-month conversation reconstruction, whole-chat RootCause/MT captures

## 1. Governing correction

Current ImprovementCore already has:
- an augmented controller C+ with learning memory and recursive child actions;
- hard admissibility before preference;
- set-valued nondominated routing;
- continuation-relative representation sufficiency;
- typed transition outcomes;
- basis-relative closure;
- discovery-sensitive reentry;
- cumulative anti-loss;
- historical replay and holdout evidence.

The remaining mathematical gap is that "strict gain" is not yet one canonical pre/post relation consumed by recurrence, no-gain memory, self-improvement admission, and closure.

That leaves room for distinct subsystems to treat different nearby states as progress:
- documented versus active;
- configured versus executed;
- selected versus consumed;
- repository-fixed versus user-visible-fixed;
- child-local close versus parent-global close;
- artifact adequacy versus method efficacy.

This candidate makes progress itself a typed mathematical object.

## 2. Improvement claims are indexed

An unqualified statement "x improved" is too weak.

Define an improvement-claim scope:

sigma =
<Target,J,K,Beta,Rho,Boundary>.

Target is the evaluation target:
ARTIFACT,
METHOD,
INTERACTION,
REDUCTION,
ACTIVATION,
HOST_BOUNDARY,
or another explicitly typed target.

J is the protected job/result.
K is the protected invariant set.
Beta is the admitted basis: evidence, authority/currentness, discovery-generator basis, search/coverage horizon, and runtime facts.
Rho is the representation family used for the comparison.
Boundary is the boundary at which the claimed effect must be observed.

The ZIP experiments establish why Target is load-bearing:

artifact adequacy != method efficacy != interaction efficacy != reduction adequacy.

Therefore evidence for one target does not automatically witness another target.

## 3. Controller state

Let h_t be admitted controller history.

Let

phi(h_t)=z_t.

A compressed z_t is authoritative only when

StateSuff_sigma(phi)

holds: equal projected states preserve every protected continuation distinction relevant to sigma.

Define augmented candidate state:

X_t =
<z_t,m_t,b_t>,

where:
- z_t is a continuation-sufficient semantic state representation;
- m_t is basis-relative learning/NoGain/rejection/failure memory;
- b_t is the explicit live basis descriptor.

Making b_t explicit prevents two states with identical visible semantic fields but different evidence, authority, representation, generator basis, or coverage horizon from being treated as the same controller state.

The current C+ is recovered as the projection that keeps b_t implicit in its semantic state and memory records.

## 4. Continuation equivalence

For states x,y under scope sigma:

x equiv_sigma y

iff every licensed protected continuation observes them equivalently with respect to:
- admissible action frontier;
- protected observations;
- nondominated policy frontier;
- execution-truth admissibility;
- retry licenses;
- protected contribution reachability;
- terminal disposition.

This induces the basis-relative semantic quotient:

Q_sigma = Hist_Beta / equiv_sigma.

Raw file differences, timestamps, IDs, or wording differences do not establish a new semantic state when they preserve the same continuation class.

## 5. Action generation and admission

Let

Gamma_sigma(x)

generate candidate actions/packages from:
- live questions and discriminators;
- relation/candidate-universe residuals;
- ProbeSig capability semantics;
- broad-corpus navigation;
- licensed compositions/interactions;
- recursive child runs;
- external acquisition when materially required.

Admission is hard-gated:

Adm_sigma(x,a)

requires:
- authority fit;
- valid inputs;
- current full invocation/wrapper profile when applicable;
- protected-transition integrity;
- execution binding;
- no unchanged NoGain block;
- lineage preservation/challenge when a successor claim is involved.

A named or registered tool is not admitted merely because it exists.

## 6. Policy remains set-valued

For admitted action/package a, retain the current gain coordinates:

Gain_sigma(a)=
<
MaterialSeparation,
DependencyLeverage,
CandidateUniverseEffect,
RelationEffect,
ReachableWorkEffect,
ContinuationValue,
FailureAvoidance,
ClosureEffect,
Burden,
Risk,
AuthorityFit
>.

Define partial dominance, not one global scalar utility.

Let

ND_sigma(x)
=
Max_≻ {a in Gamma_sigma(x): Adm_sigma(x,a)}.

A single action is selected only by an explicit licensed chooser over this nondominated frontier.

## 7. Typed transition and admission

Raw transition:

T_sigma(x,a)
subseteq
(O x Xi x X_raw) + D,

where Xi distinguishes execution truth, including:
NOT_EXECUTED,
SEMANTICALLY_APPLIED,
IMPLEMENTATION_EXECUTED,
RESULT_USED,
FULL_MATCH,
OPEN,
BLOCKED,
CONFLICT,
MISMATCH_BLOCKED.

The raw return is not authoritative state.

Normalize through the required obligation path:
raw result
-> discovery closure when required
-> consequence/tool-run closure
-> verification
-> authority/currentness admission
-> HF1
-> HF2 applicability
-> parent admission/reentry.

Only evidence at the claimed Boundary can witness a Boundary-level improvement.

## 8. Protected regression

Define

Regress_sigma(x,x')

when a material protected object is silently lost or weakened, including:
- protected behavior;
- accepted result;
- source/provenance dependency;
- authority/currentness fact;
- execution-truth distinction;
- required continuation;
- verified contribution;
- historical witness;
- hard constraint.

A loss is not silent when it is explicitly and validly dispositioned as revised, retracted, OPEN, BLOCKED, CONFLICT, or NOT_APPLICABLE under the governing authority.

Silent regression blocks a strict-gain claim even when another coordinate improves.

## 9. Effect witnesses

Let

EW_sigma(a;x,x')

be the set of causally supported, result-sensitive effects attributable to action a.

Canonical effect families include:
1. ACTION_CHANGED
2. PROTECTED_FAILURE_PREVENTED
3. LOWER_BURDEN_EQUIVALENT
4. NEW_REACHABLE_WORK
5. NEGATIVE_ROUTE_CLOSED
6. GOAL_GAP_REDUCED
7. MATERIAL_DISTINCTION_DISCOVERED
8. MATERIAL_RELATION_DISCOVERED
9. COVERAGE_STRENGTHENED
10. EXECUTION_TRUTH_STRENGTHENED
11. OPEN_RESOLVED
12. BLOCKED_RESOLVED
13. CONFLICT_RESOLVED

Every effect witness carries:
- target;
- basis id;
- evidence;
- causal route;
- claimed boundary;
- benchmark/holdout id when the claim is benchmark-relative.

An empty label with no evidence is not a witness.

## 10. Canonical strict progress relation

Define:

x <_sigma x'

iff all of the following hold:

1. not Regress_sigma(x,x');
2. EW_sigma(a;x,x') is nonempty;
3. the effect evidence reaches the boundary claimed by sigma;
4. every mandatory obligation created by the transition has a typed disposition;
5. a changed basis has been explicitly reconciled before comparison.

This relation is partial.

Two successors can remain incomparable.

A discovery that enlarges the candidate universe can still be strict progress when it creates a material distinction, relation, or newly reachable justified work.

A lower-burden successor is strict progress only when protected continuation behavior is equivalent or stronger.

A repository artifact can be an ARTIFACT gain without being an ACTIVATION or HOST_BOUNDARY gain.

## 11. Certified no-gain

Define:

NoGain_sigma(a;x,x')

iff:
- x equiv_sigma x';
- EW_sigma(a;x,x') is empty;
- the relevant basis is unchanged;
- no protected regression is hidden;
- execution truth is sufficient to certify that the route was genuinely tested.

Then store:

Neg(a)=
<NO_GAIN,Beta,DependencyFootprint,Evidence,ResultEffect=NONE>.

The unchanged route is removed from the next admissible frontier.

Retry is licensed only when a changed coordinate intersects the recorded dependency footprint, defeats the prior failure signature, changes representation/executability materially, or creates a genuinely new interaction package.

This makes negative evidence causally alter future policy.

## 12. Semantic cycle blocking

A raw state-ID change is not progress.

For k>=1, a basis-relative no-gain cycle exists when:

[x_t]_sigma = [x_(t-k)]_sigma

and:
- the relevant basis is unchanged;
- the intervening route family produces no net effect witness;
- no intervening transition resolves a protected OPEN/BLOCKED/CONFLICT state.

Record CYCLE_NO_GAIN against the implicated route dependency footprint.

The same semantic cycle is then inadmissible until its relevant basis changes.

This blocks audit-of-audit loops whose artifacts differ while continuation behavior does not.

## 13. Local and global recurrence

HF2 owns local same-capability recurrence.

HF2(c) is licensed only when:
- c produced an admitted changed successor;
- the change is continuation-relevant;
- c has a non-NoGain continuation on that changed successor.

The parent ImproveCore controller owns global recurrence.

Global recurrence occurs when an admitted transition changes a material job, relation, candidate universe, capability frontier, representation, evidence/authority basis, or protected continuation.

Child RELATIVE_CLOSE does not imply parent RELATIVE_CLOSE.

## 14. Coverage-indexed terminality

Let CoverageCert_Beta carry typed coverage dispositions for:
- work/job generation;
- capability generation;
- candidate-universe adequacy;
- relation-generator basis;
- search/policy horizon;
- historical protected witnesses;
- execution/persistence/currentness obligations.

Use typed states such as:
CLOSED,
OPEN,
BLOCKED,
CONFLICT,
NOT_APPLICABLE.

Do not manufacture percentage coverage when the generator universe is not enumerated.

Then:

Tau_sigma(x)=RELATIVE_CLOSE

only when:
- protected goal gap is zero under sigma;
- no live admitted continuation remains under Beta;
- required discovery/consequence/wrapper obligations are terminal;
- execution/persistence/currentness claims are verified at their claimed boundary;
- CoverageCert_Beta is valid;
- no protected regression remains unresolved;
- any successor-lineage obligation is dispositioned.

Resource exhaustion returns RESOURCE_STOP/OPEN, not semantic completion.

Open-world GLOBAL_MAXIMALITY and GLOBAL_MINIMALITY remain invalid completion criteria.

## 15. Fixed-basis anti-repeat theorem

Assume:
- a fixed basis Beta;
- a finite admitted route universe R;
- exact continuation-equivalence recognition for the declared scope;
- every tested unchanged no-gain route is durably recorded;
- RetryLicense requires a relevant basis/dependency change.

Then an unchanged semantic no-gain route cannot be selected indefinitely.

Proof sketch:
after its first certified NoGain receipt, the route is blocked;
under fixed Beta its retry condition remains false;
therefore it cannot re-enter the admissible frontier.

This is an anti-repeat theorem, not an open-world global termination theorem.

A stronger termination theorem additionally requires a finite/well-founded semantic quotient and a proof that every nonterminal admitted transition either strictly progresses under a well-founded relation or permanently closes at least one remaining route.

## 16. Self-improvement admission

Let C be current ImproveCore and C' a proposed successor.

C' is not an improvement merely because:
- it is newer;
- it has more files;
- it has fewer files;
- tests on one episode pass;
- it reproduces one final answer;
- it was produced by ImproveCore itself.

A preserving successor claim requires:
- FullMath/reconstruction identity;
- current wrapper/execution identity;
- protected lineage preservation;
- failure-mode-distinct challenge where self-generated;
- matched historical replay;
- unlike holdout evidence;
- strict progress C <_sigma C' for the stated evaluation target;
- no silent regression.

Self-application is therefore evidence generation, not self-certification.

## 17. ImprovementCore algebra

The earlier desire to "add", "multiply", and "divide" ImproveCore operations has a precise non-scalar interpretation.

### Sum / frontier union

A ⊕ B
=
ND_sigma(Adm_sigma(A union B)).

This means expose both action families and retain the admissible nondominated frontier.
It does not numerically add scores.

### Product / interaction

A ⊗ B
=
ND_sigma(
Adm_sigma(
{A o B, B o A} union ResidualInteract(A,B)
)
).

The product is generally noncommutative.

OrderGate determines when both A o B and B o A require exploration.

A product has strict interaction gain only when it exposes a material residual not available from either factor alone, prevents a protected failure, or produces lower burden with preserved behavior.

### Quotient / safe compression

A / equiv_sigma

collapses continuation-equivalent states/routes/representations.

This is valid only with a continuation-preservation witness.

Division is therefore quotienting by a proven equivalence relation, not deleting components because outputs looked similar once.

### Powers / repeated self-application

A^n

means repeated admitted recurrence.

No monotonicity is assumed.

Each factor must produce strict progress, justified negative closure, or a typed unresolved boundary.
A certified NoGain factor halts unchanged repetition.

## 18. Why this explains the conversation failures

The recovered conversation history repeatedly distinguishes states that older "material delta" flags can accidentally conflate.

Examples:

DOCUMENTED != ACTIVE
because ACTIVATION is a different evaluation target/boundary.

SELECTED != EXECUTED
because execution truth has not reached the claimed boundary.

EXECUTED != RESULT_USED
because consequence consumption is a further transition.

REPOSITORY_FIXED != USER_VISIBLE_FIXED
because the host-visible boundary has not been witnessed.

CHILD_CLOSE != PARENT_CLOSE
because continuation is owned at different recurrence scales.

ARTIFACT_PASS != METHOD_VALID
because evaluation target typing differs.

REGISTERED_CAPABILITY != REACHABLE_CAPABILITY
because reachability is an admission/activation fact.

These are not rhetorical distinctions. They are non-equivalent states under equiv_sigma whenever they alter a protected continuation.

## 19. Candidate controller

The proposed mathematical successor is:

C*_(J,K)
=
<X,
 D,
 Gamma,
 Adm,
 Pi,
 T,
 Ack,
 <_sigma,
 Tau>,

with:

X = <z,m,b>,

Gamma = endogenous candidate generation,
Adm = hard admission,
Pi = set-valued nondominated policy correspondence,
T = typed raw transition,
Ack = normalization/admission/obligation consumption,
<_sigma = canonical strict progress,
Tau = basis-relative terminality.

C* does not replace current C+ by declaration.

C* is admitted only if implementation and regression tests show a strict gain over C+ without loss of current protected behavior.

## 20. Open coordinates

Still OPEN:
- computable general continuation quotient for unrestricted histories;
- exact chooser from a plural nondominated frontier;
- proof of well-founded strict progress outside declared finite bases;
- scalable semantic cycle detection across arbitrary representation changes;
- quantitative information-loss measure;
- complete general problem-generation relation;
- global fairness over infinite/open frontiers;
- direct account-wide ChatGPT export corpus completeness in this run.

The last item matters because conversation-derived evidence was recovered from Take-5 conversation artifacts and the four-month reconstruction, while the exact account-export ZIP referenced by the user has not been located as a committed Git tree object or visible Library ZIP by filename.

## 21. Promotion rule

Status remains CANDIDATE.

Promotion requires executable tests for:
- documentation-only false progress;
- selected-but-not-executed false progress;
- repository-fixed-but-host-unverified false progress;
- protected witness loss;
- discovery gain;
- lower-burden equivalent gain;
- certified no-gain;
- no-gain cycle blocking;
- basis-change retry;
- local-versus-global closure separation.

No current pointer changes merely because this artifact exists.


## Longitudinal comparison companion

Regime 090 promotes this document's strict-progress relation as the local transition admission gate.

The distinct longitudinal/system comparison problem is governed by:

- `architecture/IMPROVEMENT_CORE_INDEXED_PROGRESS_MATHEMATICS_111.md`
- `runtime/improvement_core_order_math.py`

A local effect witness establishes one transition's causal, boundary-verified progress. It does not independently establish a transitive order over arbitrary controller states or across basis changes.

Longitudinal strict-improvement claims therefore use the basis-indexed preorder and, for cross-basis episodes, one admitted common `ComparisonFrame`.
