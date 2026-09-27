# ImprovementCore Recoverable OPEN Reentry 001

Date: 2026-09-27
Status: CURRENT CANDIDATE UNDER VALIDATION

## Failure

HF002 owns local recurrence of one configured capability.

That means

HF002 local close

does not imply

the parent governing problem has no reachable work.

The recurring failure occurred when a configured tool reached a local fixed point, exposed a
result-sensitive OPEN requiring another capability, and the parent classified that residual as
terminal external OPEN. The residual was then returned to the user even though a recovery route
already existed in repository history or the configured repertoire.

TransferCore exposed this defect directly.

## Parent invariant

Let o be an OPEN residual in parent state z.

Recoverable(o,z)

iff

ResultSensitive(o)
and Reachable(o,z)
and RecoveryRoute(o) is explicitly bound.

Then

Recoverable(o,z)
=> OwnedWork_ImprovementCore(o)
=> ParentReturn = CONTINUE
=> reenter the complete ImprovementCore capability.

A recoverable OPEN cannot become a user-return terminal merely because the child capability or
its HF002 recurrence has saturated.

## External boundary

An OPEN can return as a typed terminal boundary only when the current basis establishes that the
parent has no reachable recovery route under its authority.

Examples include a host that never invokes Take-5 or a genuinely unavailable external evidence
source.

The parent gate does not invent a route. A semantic producer must supply reachability and a
recovery route.

## Runtime

runtime/improvement_core_return_gate.py

The return gate reads structured open_residuals and identifies rows carrying:

result_sensitive = true

reachable = true

recovery_route = nonempty.

When such a row exists, a proposed RETURN becomes CONTINUE and the row is captured as
owned_recovery_work.

## Relation to HF002

HF002 remains unchanged.

It continues to answer:

does this same configured capability have another material local continuation under the stable
upstream basis?

ImprovementCore answers the larger question:

after that capability stops, does the governing problem expose another reachable result-sensitive
piece of work?

This separation preserves the exact HF002 object while delivering the user's intended
continue-until-the-real-job-is-finished behavior at the correct parent layer.

## Closure

Parent return is legal only after:

local configured recurrence is settled;

all reachable result-sensitive OPEN residuals have been converted to owned work and consumed;

material consequences are closed;

remaining OPEN/BLOCKED/CONFLICT coordinates have no reachable current-basis recovery route or
are governed external boundaries.

A future newly reachable route reopens only the affected cone.

This is finite basis-relative closure, not a claim of open-world completeness.
