# HF2 Fixed-Point Closure Contract

Date: 2026-10-01  
Status: ACTIVE IMPLEMENTATION CONTRACT  
Scope: every configured Take-5 tool invocation using HF002 recurrence

## Problem

The prior HF2 runtime could return RELATIVE_CLOSE immediately after a round that
reported a material delta whenever the adapter simultaneously reported no live
local frontier or returned local-close truth.

That admitted this failure mode:

X0 -> discover/mutate X1 -> RELATIVE_CLOSE

A later external invocation could then observe X1 and discover D2 that was
already derivable from the changed state. The first invocation had never
performed a clean post-mutation verification pass over X1.

## Required fixed-point semantics

Let F be one fully configured tool round and let delta_n be the admitted HF2
delta from round n.

HF2 closure is valid only at a state X* for which a verification application of
the same configured operator produces no material delta and no unresolved
frontier:

F(X*) = X*
relative to the frozen basis and configured scope.

Operationally:

1. Any material delta makes the state DIRTY.
2. DIRTY always causes another internal application of the same configured tool.
3. RELATIVE_CLOSE is forbidden while DIRTY.
4. A subsequent round must be materially clean.
5. Any live local frontier, affected frontier, unresolved scope delta, OPEN,
   BLOCKED, CONFLICT, or HF1 reentry prevents closure.
6. Only a materially clean round over the post-mutation successor can discharge
   DIRTY and establish RELATIVE_CLOSE.
7. Hitting max_rounds returns RESOURCE_STOP rather than a false closure.

Thus:

material(delta_n) => run round n+1

and

RELATIVE_CLOSE => clean(delta_n) and local_close(X_n) and
                  no_live_frontier(X_n) and no_affected_frontier(X_n).

## Affected-scope contract

Adapters may expose either of these fields:

- hf2_affected_frontier: iterable/bool describing unresolved affected scope
- hf2_scope_deltas: mapping from scope name to a truthy unresolved/material delta

Any truthy value blocks closure. This lets manuscript-aware tools represent
claim, paragraph, subsection, section, manuscript, cross-document, and control
state frontiers without hard-coding manuscript semantics into HF002.

HF2 remains generic. Domain tools own discovery of the affected cone; HF2 owns
the rule that the cone must be clean before closure.

## Escape invariant

For the same frozen basis, same configured rules, and same target state:

second external run material discovery = regression escape

The runtime prevents the most direct class of escape by requiring the clean
post-mutation pass internally. Domain-specific regression suites remain
responsible for asserting that their affected-frontier representation is
complete.

## Completion invariant

No clean pass after the final material change means the invocation is not
finished.

Formally:

CLOSED(X) iff
  clean_delta(X)
  and local_close(X)
  and not live_local(X)
  and not affected_frontier(X).

This contract is fail-closed.
