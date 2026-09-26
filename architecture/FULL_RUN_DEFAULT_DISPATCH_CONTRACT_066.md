# Full Run Default Dispatch Contract 066

Date: 2026-09-25
Status: CURRENT USER-INVOCATION CONTRACT

## Failure

A user command such as "run MT" was allowed to degrade into the bare MT semantic primitive, without the canonical wrapper and without the intended typed 36-cell geometry.

Two causes were found:

1. MT was missing from the configured-run registry even though MTA was registered.
2. No user-command boundary forced ordinary tool requests to resolve to configured runs.

## Rule

For a registered tool T:

Run(T) means the current configured execution contract.

Ordinary user phrasings such as:

- run T
- T this
- run T on this

resolve to:

Configured(T)
+ CanonicalSystemWrapper
+ tool-appropriate typed geometry
+ recursion
+ closure
+ reentry.

Bare/core execution is an explicit escape hatch only:

- run bare T
- run core T
- isolate T core

## MT binding

MT is a first-class configured tool.

Its default full geometry is:

D36_C = Scope x ModeFace

with cardinality 6 x 6 = 36.

Therefore:

run MT

does not mean one MT pass.

It means MT executed through the canonical system wrapper over D36_C, with configured recursion, closure, and reentry.

## Anti-degradation invariant

Let U be the user's invocation and R(U) the resolved run request.

For every registered tool T:

ordinary_invocation(U,T)
=> configured(R(U))
AND wrapper_required(R(U)).

For MT:

ordinary_invocation(U,MT)
=> geometry(R(U)) = D36_C.

Only explicit bare/core language licenses:

configured(R(U)) = false
AND wrapper_required(R(U)) = false.

## Consequence

A tool implementation may expose a core semantic operator internally, but user-facing dispatch cannot select it merely because the user used the short name of the tool.

## MT before-return semantic gate

Configured MT also owns a synchronous semantic-enrichment gate before user-visible return.

When MT exposes BLACK_BOX_OPEN object o:

MT(x)
-> SemanticResolutionPass(o)
-> Admit(material semantic delta)
-> re-run MT on the enriched state when the delta is result-sensitive
-> return when MT result is stable, the semantic pass yields no material delta, a stage returns OPEN/BLOCKED, or the bounded round limit is reached.

This does not require full semantic closure.

Unresolved residue remains BLACK_BOX_OPEN with retained evidence and re-enters on a later encounter.

Therefore configured "run MT" means:
- full wrapper;
- D36_C geometry;
- recursion/closure/reentry;
- synchronous bounded semantic enrichment before return.

Bare/core MT bypasses this gate.
