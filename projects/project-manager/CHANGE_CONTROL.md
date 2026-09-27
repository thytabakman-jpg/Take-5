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
