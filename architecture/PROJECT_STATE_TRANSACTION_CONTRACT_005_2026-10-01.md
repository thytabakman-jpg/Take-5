# Project State Transaction Contract 005

Date: 2026-10-01
Status: IMPLEMENTED / VALIDATION PENDING

## Job

ProjectStateTransaction makes every admitted ProjectManager mutation one coherent project state transaction.

ProjectManager continues to observe, assess, route, and produce a READY ProjectDelta without mutating project truth.

The separate commit boundary now owns the complete mutation sequence:

Freeze base
-> compute affected cone
-> bind one disposition for every affected object
-> run CurrentnessAudit
-> run Tool Run Closure
-> verify complete accounting
-> recheck repository head
-> CommitOnce
-> ICC128 reselection
-> ImprovementCore handoff for explicit unresolved residue.

## Core invariant

For admitted event e on project state P:

Committed(e)
implies
for every x in A(e,P), Accounted(x,e).

A(e,P) is the transitive affected cone:

A(e,P)
=
Changed(e)
union
Reach_plus_Dep(Changed(e)).

Every affected object receives exactly one admitted disposition from:

CURRENT
SUPERSEDED
OPEN
BLOCKED.

CONFLICT, UNKNOWN, UNVERIFIED, STALE, PENDING, missing disposition, or an unreverified currentness delta prevents commit.

## Currentness

CURRENT means either:

1. the object is already current on the bound basis, or
2. a basis delta has been explicitly represented and the patch has been reverified.

A basis mismatch with an empty delta fails OPEN.

SUPERSEDED is an explicit terminal currentness disposition.

OPEN and BLOCKED remain first class routed residue. They count as accounted consequences while remaining unresolved.

## Consequence closure

Each affected object becomes one Tool Run Closure consequence.

CURRENT objects are realized, verified, and consumed.

SUPERSEDED objects are certified no effect.

OPEN and BLOCKED objects remain typed unresolved consequences.

A commit requires complete affected cone accounting. Substantive settlement of every OPEN or BLOCKED consequence is not required for the transaction itself; those objects are routed forward as explicit obligations.

## Concurrency

Every transaction binds:

base_version
observed_head
commit_head.

If observed_head differs from base_version, the transaction recomputes the affected cone against the latest dependency graph and returns REBASE_REQUIRED.

Immediately before commit:

commit_head = base_version

is required.

A changed head produces REBASE_REQUIRED with a recomputed affected cone. The transaction never overwrites concurrent work.

## Commit

The final state authorization uses the common state_commit gate with:

role = SUPERVISORY
effect = PROJECT_STATE_TRANSACTION_COMMIT_ONCE.

There is one commit authorization after complete affected cone accounting.

## ICC128 reentry

A successful material transaction emits a material state delta to the current rho128 reselection predicate.

The transaction therefore requires ICC128 reselection after commit.

## ImprovementCore relation

Explicit OPEN and BLOCKED affected objects are returned as an evidence only ImprovementCore handoff frontier.

ImprovementCore can work those obligations. Its output still requires the same ProjectManager admission and transaction path before becoming project truth.

## ProjectManager relation

runtime/project_manager.py exposes project_manager_commit_transaction.

The function accepts only READY ProjectDelta objects whose precondition fingerprint still matches the current project package.

Normal ProjectManager adapter output also identifies this transaction path whenever a READY delta exists.

## Implementation

runtime/project_state_transaction.py

runtime/project_manager.py

runtime/currentness_audit.py

runtime/tool_run_closure.py

runtime/state_commit.py

runtime/rho128_policy.py

## Verification

tests/test_project_state_transaction.py verifies:

recursive affected cone generation
complete affected object accounting
missing disposition failure
unreverified currentness failure
explicit OPEN and BLOCKED routing
head drift recomputation
stale base recomputation
single CommitOnce authorization
ICC128 reselection
ProjectManager READY delta integration.

Repository validation, capability preservation, and the configured tool portfolio remain promotion gates.
