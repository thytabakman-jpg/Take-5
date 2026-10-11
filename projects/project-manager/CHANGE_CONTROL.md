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

A target-transforming delta requires a transformation-class operation plus explicit authority,
a represented consequence/impact map, and named regression-verification tests before
it can become READY. The native `route_event` applies these checks to a proposal;
READY does not execute, verify, admit, or persist the transformation.

`precondition_fingerprint` records the exact project basis at proposal time. The
admitting/writing owner must reject or reopen a stale fingerprint before applying
any delta to changed state. Do not infer compare-and-swap enforcement merely from
the field's presence in the observer result.

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
