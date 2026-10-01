# Change control

Status: CURRENT

ProjectDelta =
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

## Rules

Route the request to the smallest canonical owner set that actually owns the affected object.

Recovery and evidence work may proceed while a coordinate is OPEN.

A target-transforming delta requires a transformation-class operation plus explicit authority.

After a material admitted delta, inspect direct dependents, interfaces, risks, verification,
lifecycle state, open questions, decisions, lessons, handoffs, and affected coverage evidence.

Preserve unaffected accepted state.

A stale precondition fingerprint reopens the delta instead of applying it to a changed project.


## Pre-project promotion control

A candidate definition is not a project mutation.

DefinitionReady records that the compact definition is sufficiently resolved for a human decision.

PromotionReady requires explicit USER approval.

Only a later separately admitted PROMOTE transition can create the full project package.

A tool output, automated controller, or newer artifact cannot substitute for that approval.


## Project state transaction gate

Every READY ProjectDelta uses project_manager_commit_transaction.

The transaction binds the base version, computes the full transitive affected cone, and requires one typed disposition for every affected object.

Allowed accounted dispositions are CURRENT, SUPERSEDED, OPEN, and BLOCKED.

CURRENT with a changed basis requires an explicit delta plus reverified currentness.

The transaction runs Tool Run Closure across the affected cone and authorizes exactly one PROJECT_STATE_TRANSACTION_COMMIT_ONCE after complete accounting.

A base or head mismatch recomputes the affected cone against the latest supplied dependency graph and returns REBASE_REQUIRED.

Every successful material commit forces ICC128 reselection.

Explicit OPEN and BLOCKED residue is routed to ImprovementCore as evidence-only work and remains subject to the same admission path for later mutation.
