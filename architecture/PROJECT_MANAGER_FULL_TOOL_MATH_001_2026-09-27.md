# ProjectManager Full Tool Mathematics 001

Date: 2026-09-27
Status: ACCEPTED FOUNDATIONAL LAYER / ORIGINAL PR 164 MERGED
Status at original promotion: CURRENT / VALIDATED / MERGED
Lineage: PR 164 merged as 4d8477dd79e45292e9f8f736721b97eedb23f054.
Later additive layers: 002 (admission), 003 (management spine), 004 (failure immunity).
This historical foundational object remains valid as a layer, not the sole
live configured identity. Resolve current implementation through the
ProjectManager controller and runtime/tool_manifest.py, not its filename suffix.
Canonical target: thytabakman-jpg/Take-5
Project self-instance: projects/project-manager/

## Table of contents

- [1 Job](#1-job)
- [2 Governing question](#2-governing-question)
- [3 Native project state](#3-native-project-state)
- [4 Tool object type](#4-tool-object-type)
- [5 Observer run and commit separation](#5-observer-run-and-commit-separation)
- [6 Event and delta](#6-event-and-delta)
- [7 Work package](#7-work-package)
- [8 Authority invariant](#8-authority-invariant)
- [9 Decomposition invariant](#9-decomposition-invariant)
- [10 Locality and impact](#10-locality-and-impact)
- [11 Full tool identity](#11-full-tool-identity)
- [12 Geometry](#12-geometry)
- [13 Protected behaviors](#13-protected-behaviors)
- [14 Closure](#14-closure)
- [15 Self-management](#15-self-management)
- [16 ImprovementCore relation](#16-improvementcore-relation)
- [17 TransferCore relation](#17-transfercore-relation)
- [18 Requested bootstrap sequence](#18-requested-bootstrap-sequence)
- [19 Full configured invocation](#19-full-configured-invocation)
- [20 Nonclaims](#20-nonclaims)

## 1 Job

ProjectManager keeps a project identifiable, authority-bound, current, decomposed,
traceable, and legally changeable while preserving accepted state and exposing the
next executable work frontier.

It is not the project's domain solver.

## 2 Governing question

For project p and incoming event e:

What project state is actually current, what remains between that state and the
governing goal, and what is the next legal bounded project transition or work package
that advances the goal while preserving authority, accepted state, dependencies,
risks, decisions, evidence, and OPEN coordinates?

## 3 Native project state

Let

C_PM =
{
identity,
charter,
goal,
scope,
authority,
stakeholders,
deliverables,
schedule,
resources,
dependencies,
interfaces,
raid,
questions,
evidence,
decisions,
lessons,
changes,
lifecycle,
verification,
communications,
handoffs
}.

These are native project-state coordinates. They are not the 36 configured-run cells.

For each c in C_PM let X_c be the admissible state space of that coordinate.

P_PM = Product_(c in C_PM) X_c.

A managed project state is p in P_PM plus a project identifier and an authority registry.

The state space is extensible. A project can add domain-specific coordinates without
silently deleting the core coordinates.

## 4 Tool object type

ProjectManager is a typed authority-governed nondeterministic labeled transition
system with a supervisory frontier policy:

PM
=
<
P_PM,
E,
W,
Gamma,
Pi,
Delta_PM,
Omega,
Inv,
Kappa
>.

P_PM = managed project states.
E = project events/evidence/requests.
W = typed work packages.
Gamma = authority, admission, effect, and precondition guard.
Pi = routing and executable-frontier policy.
Delta_PM subseteq P_PM x E x W x P_PM x Receipt is the legal transition relation.
Omega = observation and receipt function.
Inv = protected project-management invariants.
Kappa = relative-closure and reentry predicate.

The relation is intentionally not forced into a total deterministic function. Multiple
live work packages, OPEN, BLOCKED, and CONFLICT remain representable.

## 5 Observer run and commit separation

Configured tool execution is observer-only:

PM_obs(p,e)
=
<
Assessment,
ExecutableFrontier,
DeltaCandidate,
Handoffs,
Status,
Receipt
>.

PM_obs does not mutate canonical project truth.

A state-changing project commit is separate:

Commit(p,d,a) = p'

only when Gamma(p,d,a)=PASS and the owning authority plus project change-control path
admit the transition.

This preserves the global Take-5 rule that a tool run does not self-authorize mutation.

## 6 Event and delta

Project event:

e
=
<
event_id,
request,
affected_coordinates,
source,
evidence,
operation_class,
effect_class,
authority_ref
>.

Project delta:

d
=
<
event_id,
owners,
affected_coordinates,
precondition_fingerprint,
request,
reason,
dependencies,
impact_coordinates,
tests,
authority_ref,
effect_class,
status
>.

This generalizes the project-local change object recovered from the Sukkos project.

## 7 Work package

w
=
<
work_id,
target_coordinate,
target_object,
operation_class,
effect_class,
dependencies,
tool_id,
success,
tests,
authority_ref,
status
>.

Executable(p,w)
iff
StructurallyComplete(w)
and DependenciesClosed(p,w)
and EffectLicensed(w)
and target_coordinate(w) in C_PM
and status(w) notin {COMPLETE,CLOSED,SUPERSEDED,BLOCKED,CONFLICT}.

The executable frontier is set-valued. ProjectManager does not invent a scalar ranking
when multiple incomparable work packages remain live.

## 8 Authority invariant

For every mutable project object o:

|Owner_p(o)| = 1

is required for an authoritative change route.

Zero owners yields OPEN.
More than one owner yields CONFLICT.

A single file may own several explicitly declared objects. A mutable object may not have
several competing canonical owners.

Recency alone never creates authority.

## 9 Decomposition invariant

Deliverable decomposition and schedule are distinct objects.

WBS(p) != Schedule(p).

The WBS owns what deliverables constitute total project scope.
Schedule owns temporal ordering, dates, cadence, and milestones.

Collapsing them into one authority is a control conflict for the core project package.

## 10 Locality and impact

For event e:

OwnerTargets(e)
=
Union_(c in affected(e)) Owner_p(c).

A legal delta changes only the smallest owning object set required by the event.

After an admitted material delta d:

Impact(d)
-> VerifyDirectDependents
-> VerifyInterfaces
-> VerifyProtectedState
-> UpdateLifecycle
-> RecordDecision
-> RecordLesson when failure/learning occurred
-> RecomputeFrontier
-> Reenter.

No clean rebuild is licensed merely because one coordinate changed.

## 11 Full tool identity

Under the current full-tool contract:

FullMath_(J,K)(ProjectManager)
=
<
N_PM,
W_PM,
G_PM,
P_PM_tool,
L_PM
>.

N_PM
=
<
Type,
Dom,
Cod,
State,
Graph,
Adm,
Obs
>

with Type equal to the authority-governed nondeterministic labeled transition system
defined above.

W_PM = G_Tool(W^-_PM,W^o_PM,W^+_PM,W^x_PM).

W^-_PM:
bind project identity
-> load project package
-> bind current governing goal
-> bind authority/currentness
-> validate required coordinates
-> preserve OPEN/CONFLICT.

W^o_PM:
run native project-state audit
-> compute executable frontier
-> route bounded event/delta
-> map impact/dependencies/interfaces
-> emit ImprovementCore and transfer evidence handoffs
-> preserve plural work frontier.

W^+_PM:
verify result and impact
-> Tool Run Closure
-> update only through separate admitted commit
-> recompute project state/frontier
-> HF002 local recurrence
-> HF001 or parent-controller reentry when upstream state changes.

W^x_PM:
cross-project learning candidates
-> Transfer evidence boundary
-> target-side admission only after TransferCore identity/currentness is recovered;
substantive unresolved project work
-> ImprovementCore handoff;
project-specific domain tools
-> configured-tool execution boundary.

## 12 Geometry

G_PM
=
<
Scope,
Mode,
Order,
Arity,
Representation,
Scale,
Coverage
>.

Current configured geometry is D36_C:

D36_C = Scope x ModeFace

with six scopes:
SYSTEM,
SUBSYSTEM,
COMPONENT,
INTERFACE,
BOUNDARY_DECOMPOSITION,
CROSS_LAYER

and six mode faces:
EXPAND,
CONTRACT,
INWARD,
OUTWARD,
ISOLATE,
COUPLE.

|D36_C| = 36.

Every current full configured invocation also carries:
22 question families x 36 cells = 792 question projections;
4 cognitive operators x 36 cells = 144 cognitive projections.

The 21 native project-state coordinates and the 36 configured coverage cells are
different mathematical objects.

## 13 Protected behaviors

P_PM_tool protects at least:

1 PROJECTMANAGER_PROJECT_IDENTITY_BINDING.
2 PROJECTMANAGER_PROJECT_PACKAGE_VALIDATION.
3 PROJECTMANAGER_SINGLE_OWNER_AUTHORITY.
4 PROJECTMANAGER_LOCAL_CHANGE_ROUTING.
5 PROJECTMANAGER_OPEN_PRESERVATION.
6 PROJECTMANAGER_WBS_SCHEDULE_SEPARATION.
7 PROJECTMANAGER_IMPACT_REENTRY.
8 PROJECTMANAGER_SELF_MANAGEMENT.
9 PROJECTMANAGER_IMPROVEMENTCORE_HANDOFF.
10 PROJECTMANAGER_TRANSFERCORE_EVIDENCE_ONLY.

Generic Take-5 protections remain inherited:
configured wrapper,
Tool Run Closure,
reentry,
OPEN preservation,
Protected Transition Integrity,
HF002 recurrence,
full configured invocation profile.

## 14 Closure

ControlClose_J(p)
iff
all required project-package coordinates for J are present or explicitly typed OPEN
and every affected mutable object has exactly one canonical owner
and all admitted deltas for J are verified/accounted
and every owned executable control action for J is consumed
and every remaining unresolved coordinate is typed OPEN/BLOCKED/CONFLICT with resume condition
and the current state, decisions, evidence, and frontier agree.

ControlClose is not project completion.

## 15 Self-management

The first managed project is the tool itself.

p_PM-self in P_PM.

No special bypass exists for self-management. The ProjectManager project has its own
charter, goal, authorities, WBS, schedule, resources, dependencies, interfaces, RAID,
questions, evidence, decisions, lessons, changes, lifecycle, verification,
communications, handoffs, coverage records, and tool-run receipts.

## 16 ImprovementCore relation

ProjectManager and ImprovementCore have different jobs.

ProjectManager:
maintain coherent project control state and legal transition surfaces.

ImprovementCore:
discover/select/execute substantive improvement or research work, preserve learning,
and continue until its governing problem is relatively closed or typed OPEN/BLOCKED/CONFLICT.

ProjectManager may emit an evidence-only work frontier to ImprovementCore.
ImprovementCore may return results as evidence.
Those results do not become project truth until ProjectManager routes them through the
owning authority and admitted change path.

## 17 TransferCore relation

The requested TransferCore link is fail closed.

Current Take-5 does not contain a recovered current FullMath identity for TransferCore.

Therefore the only admitted interface in this version is:

ProjectManager
-> TransferEvidenceCandidate(effect=EVIDENCE_ONLY, grants_authority=false)
-> OPEN_TRANSFERCORE_IDENTITY

until a current recovered TransferCore identity and target-side admission path exist.

No transfer candidate can mutate a target project or self-authorize reuse.

## 18 Requested bootstrap sequence

The requested semantic sequence is preserved in:
projects/project-manager/tool-runs/.

The current HF002 contract is same-capability local recurrence. It is not a generic
cross-tool composition operator.

Therefore the user's outer-wrap intent is implemented as:

Sequence =
ASSERT
-> MT
-> HF002[ASSERT]
-> HF002[GOAL]
-> ASSERT.

OuterSequence =
Fix_material_delta(Sequence)

under ProjectManager/ICC supervisory reentry.

Each ordinary configured tool still receives its own mandatory HF002 recurrence.

This preserves the requested repeat-until-no-new-material-discovery behavior without
redefining HF002.

## 19 Full configured invocation

Ordinary invocation:

FullInvoke(ProjectManager,x)
=
HF002[
  Adapter_ProjectManager(
    Plan(ProjectManager),
    x
  )
].

Plan includes wrapper, OBSERVER, D36_C, native layer, 22 question families,
four cognitive operators, closure, reentry, OPEN preservation, PTI, and recurrence.

## 20 Nonclaims

This artifact does not claim:
universal host interception;
that every project uses identical domain-specific authority files;
that all projects need every optional PM technique;
that TransferCore is recovered/current;
that ProjectManager replaces ImprovementCore;
that control closure equals project completion;
that 21 native coordinates are 21 independent dimensions;
that 36 coverage cells are 36 native project dimensions.
