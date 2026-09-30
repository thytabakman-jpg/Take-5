# ProjectManager Full Tool Mathematics 004

Date: 2026-09-30
Status: CANDIDATE / RAISE-THE-CEILING SUCCESSOR
Supersedes on promotion:
architecture/PROJECT_MANAGER_FULL_TOOL_MATH_003_2026-09-27.md

## Governing problem

PM003 can correctly manage a well-formed project, but the cross-project failure
history shows a stronger requirement: ProjectManager must detect and route the
conditions that historically made projects malformed, stale, falsely complete,
non-executed, weakly propagated, artifact-unsafe, or dependent on human memory.

## Preserved object

The prior managed-project state remains:

P = <I,C,G,S,A,H,D,T,R,N,F,Q,E,V,L,X,Y,Z,K,M,J>

The pre-project definition state remains unchanged.

The mandatory configured management spine remains unchanged:

ASSERT
-> GOAL_pre
-> MT
-> PD
-> PDAudit
-> GOAL_post
-> CurrentnessAudit
-> QuestionWorthAsking.

All prior USER promotion, single-owner, WBS/schedule, OPEN preservation,
ImprovementCore, TransferCore, D36_C, wrapper, closure, reentry, and HF002
protections remain protected.

## Failure-prevention extension

Add the known-failure control vector

K = <k_1,...,k_17>

with the control ids defined in:

projects/project-manager/FAILURE_PREVENTION_MATRIX.md

and root-invariant vector

R = <r_1,...,r_5>.

Define:

Integrity(P)
=
Closed(K)
and Closed(R).

For every required control c:

Closed(c)
iff
status(c) in {CURRENT, NOT_APPLICABLE}
and Owner(c)
and Evidence(c)
and (
  status(c)=NOT_APPLICABLE -> Reason(c)
)
and (
  status(c)=CURRENT -> RegressionTest(c)
).

Missing, invalid, OPEN, BLOCKED, STALE, PENDING, UNKNOWN, or UNVERIFIED yields OPEN.
CONFLICT yields CONFLICT.

## Remediation frontier

A missing/open/invalid integrity obligation becomes bounded evidence work rather
than disappearing into prose.

Remediate(P)
=
{w_c | c in OpenIntegrity(P)}.

Each w_c is EVIDENCE_ONLY and routes to the corresponding canonical project
coordinate. ProjectManager therefore handles the integrity gap without granting
itself authority to rewrite the target project.

## Transform gate

For target transform event e:

TransformReady(e,P)
iff
TransformOperation(e)
and AuthorityRef(e)
and ImpactMap(e)
and RegressionVerification(e)
and PreconditionFingerprint(P).

Therefore a requested mutation with no impact map or no regression-verification
evidence is OPEN even when the requested edit itself is clear.

## State-currentness gate

For every project coordinate q with explicit lifecycle status:

q.status in
{OPEN,BLOCKED,STALE,PENDING,UNKNOWN,UNVERIFIED,CONFLICT}

prevents CLOSED_RELATIVE.

Presence of a coordinate is not evidence that its state is current.

## Frontier closure correction

PM003 permitted a semantic mismatch in which executable_frontier could be
nonempty while the aggregate status remained CLOSED_RELATIVE.

PM004 requires:

CLOSED_RELATIVE(P)
-> ExecutableFrontier(P) = empty.

More fully:

Close_PM(P)
iff
PackageValid(P)
and Integrity(P)
and StateCoordinatesClosed(P)
and ExecutableFrontier(P)=empty
and BlockedWork(P)=empty
and AuthorityConflict(P)=empty
and PendingDelta(P)=empty
and SpineClose(P).

## Five root invariants

r1 RepresentationAuthorityExecutionSeparated
r2 StateExternalizedBeforeAction
r3 MandatoryTransitionPath
r4 ClosureScopeTyped
r5 HumanNotFinalIntegrationLayer

These are closure obligations, not commentary.

## Raise-the-Ceiling strict-gain test

Let B003 be the protected behavior set of PM003 and B004 that of PM004.

StrictGain(PM004,PM003)
iff
B003 subseteq B004
and KnownFailureCoverage(PM004)=17/17
and RootInvariantCoverage(PM004)=5/5
and FalseCloseFrontierEliminated
and TransformPreflightTotal
and SelfManagementPASS
and AllToolsICC128ToolConductorPASS
and CapabilityPreservationPASS
and RepositoryValidationPASS.

## Operational guarantee

For the currently observed historical failure universe H_2026-09-30:

For every h in H_2026-09-30,

Managed_PM004(h)
->
Prevented(h)
or ExplicitOPEN(h)
or ExplicitCONFLICT(h).

No known h is licensed to pass silently as CLOSED_RELATIVE.
