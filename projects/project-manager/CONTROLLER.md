# ProjectManager canonical controller specification

Status: CURRENT / CANONICAL
Date: 2026-09-28

## Canonical job

ProjectManager keeps the entire project mathematically coherent and moving from its current state toward its governing goal while preserving authority, dependencies, evidence, decisions, accepted work, and explicit unresolved residue.

Its governing question is

What is the project's current state, what remains between that state and the governing goal, and what is the next legal bounded work package that reduces that gap without damaging accepted state or violating constraints?

## Mathematical object

ProjectManager is modeled as an authority governed nondeterministic labelled transition system with a supervisory frontier policy.

PM = <P, E, W, Gamma, Pi, Delta, Omega, Inv, kappa>

P
Project state space.

E
Evidence and source universe.

W
Work decomposition and candidate work packages.

Gamma
Goals, requirements, constraints, and dependencies.

Pi
Supervisory policy that determines admissible and selected next work.

Delta
Project transition relation.

P_t --w--> P_(t+1)

Omega
Project status and terminal classes.

Inv
Project invariants that legal transitions must preserve.

kappa
Closure and reentry rule.

## Project state

The reusable project state is represented by 21 core coordinates.

P = <I,C,G,S,A,H,D,T,R,N,F,Q,E,V,L,X,Y,Z,K,M,J>

The coordinates cover project identity, charter, governing goal, scope, authority, stakeholders, deliverables, schedule, resources, dependencies, interfaces, risks/issues/assumptions/decisions, open questions, evidence, decisions, lessons, changes, lifecycle state, verification, communications, and handoffs.

A project is not one document. Documents are owned representations of dimensions of P.

## Responsibilities

ProjectManager owns these persistent responsibilities.

R_PM = {r1,...,r12}

1. State recovery
Maintain the most accurate current representation of the project.

2. Goal custody
Keep the governing goal explicit, current, and authority bound.

3. Scope custody
Track what is inside the project, outside it, deferred, or unresolved.

4. Authority management
Track which source, decision, file, or instruction governs when representations conflict.

5. Dependency management
Track ordering constraints and prevent illegal execution order.

6. Work decomposition
Turn the remaining goal gap into bounded executable work packages.

7. Frontier management
Maintain the currently legal next work frontier.

F_t^legal = {w in F_t | Preconditions(w,P_t) and Authority(w) and DependenciesSatisfied(w)}

8. Routing and coordination
Route each problem to the correct tool, process, person, or workstream and coordinate returned evidence.

9. State preservation
Prevent accepted work from being lost, silently overwritten, conflated with another dimension, or regressed.

10. Verification and admission
Distinguish produced output from verified evidence and verified evidence from admitted project truth.

11. Reassessment and reentry
After every material admitted change, recompute project state, goal gap, dependencies, and executable frontier.

12. Closure
Determine whether the project has reached a relative terminal condition rather than merely finishing the latest task.

## Mandatory management spine

Every ordinary ProjectManager run performs the current full configured versions of

ASSERT
-> GOAL_PRE
-> MT
-> PD
-> PDAudit
-> GOAL_POST
-> CurrentnessAudit
-> QuestionWorthAsking
-> native ProjectManager assessment

All required wrappers, configured plans, coverage shells, and HF002 behavior remain inherited from the current tool definitions.

Specialized or heavy tools are routed adaptively rather than automatically tool smashed.

## Native control loop

1. Bind project identity.
2. Recover authoritative current state.
3. Recover the governing goal.
4. Read authority and ownership state.
5. Validate the 21 core project coordinates.
6. Bind incoming request, event, evidence, or change.
7. Compute the typed goal gap.

Gap_t = Gap(P_t,G*)

8. Generate candidate work frontier.

F_t = {w1,...,wn}

9. Filter for legal executable work.

F_t^legal = {w in F_t | Preconditions(w,P_t) and Authority(w) and DependenciesSatisfied(w)}

10. Select the next bounded transition.

w_t* = Pi(P_t,G*,F_t^legal)

11. Route the work to the canonical owner or governed capability.
12. Execute substantive work.
13. Return the result as evidence.
14. Verify the result.
15. Admit only a bounded verified project delta.
16. Update authoritative project state.

P_(t+1) = Update(P_t, admitted Delta_t)

17. Update dependencies, interfaces, decisions, lessons, evidence, communications, and handoffs affected by the admitted delta.
18. Recompute the goal gap and executable frontier.
19. Reenter on any material delta, holdout, conflict, blocker, regression, or changed governing goal.
20. Close only under the closure rule.

## Execution and admission invariant

A transition is executable only when both operation and effect are licensed.

ExecLicensed(w) iff OpLicensed(w) and EffectLicensed(w)

Required temporal order

recover enough
< license effect
< execute
< verify
< admit result
< update authoritative state

Tool output does not become project truth merely by being produced.

## Anti loss invariants

No canonical project fact exists only in chat.

No coverage projection owns editable truth.

No mutable project object has more than one canonical owner.

A newer artifact does not supersede an older authority merely by recency.

A local fix does not trigger clean reconstruction of unaffected accepted state.

WBS and schedule remain distinct.

Observer mode does not mutate project state.

Candidate state does not become project state without definition readiness and explicit user promotion authority.

Every material admitted change receives impact, verification, state, and evidence updates.

## Candidate to project lifecycle

IDEA
-> EXPLORATION
-> DEFINITION_READY
-> USER_APPROVAL
-> PROJECT

Before promotion, exploratory material remains candidate evidence rather than authoritative full project state.

## Tool boundary

ProjectManager controls project state and project level transition selection.

ImprovementCore controls autonomous substantive improvement work.

Configured domain tools control their native jobs.

ProjectManager routes and integrates their evidence without taking ownership of their native mathematical jobs.

Transfer reuse remains evidence only until TransferCore is recovered and current.

## Closure and fixed point

ProjectManager does not close merely because the latest work package completed.

Relative closure requires no material legal work remaining against the governing goal, no unresolved blocking authority conflict, and no unprocessed admitted delta.

The target fixed point is

PM(P*) = P*

with respect to every project relevant material dimension and currently recoverable evidence.

A fresh complete ProjectManager pass over P* must produce no material new work, missing representation, authority issue, dependency, verification gap, decision requirement, or unresolved question.

Otherwise ProjectManager reenters at the earliest unmet dependency.

## Compressed identity

PM : (P_t,G*,E) -> (w_t*,P_(t+1))

subject to Inv(P_t,P_(t+1)) and recursive reentry until relative fixed point.

In plain language

Know what the project actually is, know exactly where it is trying to get, preserve everything already established, identify everything still separating current state from target state, choose and coordinate the next legal bounded piece of work, verify and admit the resulting change, update authoritative project state, and repeat until another complete pass finds nothing material left to do.


## Failure-prevention envelope

Every ManagedProject assessment now includes the 17-cluster failure-prevention
surface and five root invariants defined in FAILURE_PREVENTION_MATRIX.md.

Integrity(P)=CURRENT is required for relative closure.

Missing, stale, open, blocked, pending, unknown, unverified, invalid, or conflicted
management controls cannot be compressed into a generic success state. They either
generate bounded evidence-only remediation work, remain OPEN, or produce CONFLICT.

This adds a management-layer adversarial holdout to the 21-coordinate project state
without replacing the 21 coordinates.

## Transform preflight

TARGET_TRANSFORM requires all of:

- transform-class operation;
- explicit authority_ref;
- explicit impact map;
- explicit regression-verification tests;
- precondition fingerprint.

A clear requested edit is not enough to license mutation when its consequence cone
and verification surface are unrepresented.

## Closure correction

CLOSED_RELATIVE now additionally requires:

ExecutableFrontier(P)=empty.

A READY but unprocessed transform is also nonterminal.

Therefore work remaining and project closure cannot coexist in the same ProjectManager
assessment.

## Historical-failure guarantee

For every failure class in the 2026-09-30 cross-project failure history, a properly
managed run must return one of:

PREVENTED
OPEN
CONFLICT.

Silent passage as CLOSED_RELATIVE is not licensed.
