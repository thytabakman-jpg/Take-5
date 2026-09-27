# ProjectManager Full Tool Mathematics 002

Date: 2026-09-27
Status: VALIDATED CANDIDATE / PR MERGE PENDING
Supersedes for current admission work: PROJECT_MANAGER_FULL_TOOL_MATH_001_2026-09-27.md
Canonical target: thytabakman-jpg/Take-5

## 1 New result-sensitive problem

The validated ProjectManager controls a project after project identity and the full project
package exist.

A new failure mode was observed:

interesting idea
-> immediate full project creation
-> large architecture and artifact population
-> later discovery that the user had not yet approved the project's highest-level identity.

This is not a domain-solver failure.
It is a missing project-admission state.

## 2 Sum-type extension

The ProjectManager input domain becomes:

PMInput = ProjectDefinitionCandidate + ManagedProject.

ManagedProject keeps the existing 21-coordinate state unchanged.

A pre-project candidate is:

D0 = <G,C,K,M,R,E,B,A,O>.

G
governing goal candidate.

C
core intellectual or product object.

K
context binding: why this domain, vehicle, or setting materially belongs.

M
mechanism producing the target change.

R
coarse causal route.

E
observable evidence of success.

B
boundaries and protected inherited state.

A
alternatives or comparator set.

O
typed open questions.

The runtime names these coordinates:

goal
core_object
context_binding
mechanism
route
evidence
boundaries
alternatives
open_questions.

## 3 Readiness and promotion

DefinitionReady(d)
iff
all nine coordinates are present
and every required non-open coordinate is nonempty
and BlockingOpen(d)=empty
and the candidate is internally coherent enough for the current job.

Human approval remains a separate authority event.

PromotionReady(d)
iff
DefinitionReady(d)
and HumanApprovalRef(d) is explicit USER authority.

Therefore:

DefinitionReady != HumanApproved.

Tool confidence, ImprovementCore output, ProjectManager output, or recency cannot impersonate
human approval.

## 4 Promotion barrier

Before PromotionReady:

candidate work is EVIDENCE_ONLY.

No full project package is created.
No WBS, schedule, exact copy, render system, or other full-project surface is required.
Exploration can still be durable.

After PromotionReady:

a separate admitted PROMOTE transition can create a full project package.

The observer run never performs that mutation itself.

## 5 Protected behavior

New protected behavior:

PROJECTMANAGER_PREPROJECT_ADMISSION_GATE.

It preserves:

IDEA != PROJECT.
DEFINITION_READY != HUMAN_APPROVED.
EVIDENCE_ONLY != TARGET_TRANSFORM.
CANDIDATE_STATE != FULL_PROJECT_STATE.
EXPLORATION_PERSISTENCE != PROJECT_PROMOTION.

## 6 Requested tool sequence

The discovery sequence is:

MT
-> PD
-> GOAL
-> GOAL.

Each factor uses the current FULL_CONFIGURED_HF2_V1 identity, D36_C, 792 question
projections, 144 cognitive projections, observer mode, closure, reentry, PTI, and its registered
HF002 recurrence.

Current HF002 is same-capability recurrence, so a literal HF002 around a heterogeneous sequence
would redefine HF002.

The lawful outer equivalent is:

Outer = Fix_material_delta(MT -> PD -> GOAL -> GOAL)

under ProjectManager/ICC supervisory reentry.

The regression witness executes the full sequence twice and requires the second normalized
result to be identical.

## 7 ImprovementCore result

The largest safe architectural change is not a new competing controller.

It is a pre-project branch inside ProjectManager:

ProjectDefinitionCandidate
-> explore and refine
-> DEFINITION_READY
-> explicit USER approval
-> PROMOTION_READY
-> separate admitted project creation.

This preserves the already validated 21-coordinate managed-project object.

## 8 Nonclaims

This does not prove that nine coordinates are globally minimal for every possible project.

It does not automate human approval.

It does not convert candidate evidence into project authority.

It does not require every exploratory idea to become a project.

It does not alter the existing Sukkos Question Booklet project.

## 9 Validation target

The change is current only after:

the new runtime tests pass,
the full configured sequence witness passes,
the existing ProjectManager tests pass,
the 93-tool ProjectManager HF2 campaign still closes relatively,
the full Take-5 validation suite passes,
capability preservation passes.


## 10 Validation receipt

Implementation head:
a02e613b3c432f93ebe86067cf763fea4d2f34e4

Take-5 Validation:
36349707998 SUCCESS.

Capability Preservation:
36349708034 SUCCESS.

Tool System Every-Tool Sweep:
36349708182 SUCCESS.

All three validation surfaces passed on the implementation head.
