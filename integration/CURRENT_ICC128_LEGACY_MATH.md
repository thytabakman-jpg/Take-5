# CURRENT ICC128 LEGACY MATH — Portable Reconstruction 001

Date: 2026-09-26
Status: VALIDATED CANDIDATE / FAIL-CLOSED
Frozen source: thytabakman-jpg/Reaserch@e4c76c595b44a35fd9efc02cde8979e656ef54e8

## Result

ICC128 Legacy contains two distinct mathematical objects.

1. Frozen controller core

ICC_128 = C_128(Z_t,F_128,MI_t)

with the endogenous loop

G_Q -> G_W -> S -> E -> A -> U -> G_Q

and the frozen rho_128 policy.

2. Take-5 Legacy activation wrapper

The frozen core plus mandatory learning-report persistence and a GitHub commit
receipt before the Take-5 run is considered closed.

These are not interchangeable because persistence is a FullMath coordinate.

## Exact higher-order boundary

The frozen runtime is intentionally higher-order. It receives:

<G_Q,G_W,S,E,A,U,DCC>

as bindings.

Therefore a complete portable mathematical reconstruction must expose those
bindings rather than inventing hidden implementations.

Current typed host primitives are:

- semantic reasoner for G_Q/G_W;
- package compiler for rho_128 selection;
- execution interface E;
- admission binding A;
- update binding U;
- discovery-closure binding DCC when discovery-sensitive deltas occur.

Missing a required host primitive is BLOCKED, not a license for substitution.

## Portable realization

Standalone reference realization:

runtime/icc128_legacy_portable.py

It has no Take-5/Reaserch imports.

Fresh-environment regression:

tests/test_icc128_legacy_portability.py

The regression copies only that file to a temporary directory and executes it in
a fresh Python process.

## SHOW_ME_THE_MATH result

For the frozen controller core:

ShowMathComplete = GREEN

when the host supplies all typed higher-order bindings.

Without a semantic reasoner or another required higher-order binding:

ShowMathComplete = RED(unavailable primitive).

For the exact Take-5 Legacy activation in an unrelated environment with no
Take-5 GitHub report sink:

ShowMathComplete = RED(GitHubReportCommitReceipt unavailable).

This is not a defect in the frozen controller. It is a wrapper/persistence
identity boundary.

## Portability conclusion

A brand-new reasoning chat can reconstruct and run the frozen controller core
from the portable mathematics without repository or conversation history by
instantiating the typed host bindings from its own reasoning/execution
environment.

Literal pure mathematics does not execute on a machine that lacks an
interpreter/reasoner. Exact Take-5 Legacy closure additionally requires the
Take-5 report receipt and therefore is not universally host-independent.


## Validation evidence

Take-5 Validation:
36260658857 SUCCESS

Capability Preservation:
36260658917 SUCCESS

The validated branch tested the current SHOW_ME_THE_MATH evaluator, isolated
single-file execution, missing-semantic-provider failure, missing-controller-binding
failure, and the exact Take-5 GitHub report-sink boundary.
