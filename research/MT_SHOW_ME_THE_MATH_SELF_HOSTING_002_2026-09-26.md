# MT — SHOW_ME_THE_MATH self-hosting repair 002

Date: 2026-09-26
Status: MATERIAL_YIELD / REPAIR SPECIFIED
Configured tool: MT
Mode: OBSERVER
Geometry: D36_C
Target: SHOW_ME_THE_MATH applied to SHOW_ME_THE_MATH
Multi-tool coverage: ToolConductor current exhaustive repertoire

## Input failure

The first self-application returned RED because the checker made these universal:

RunSpec,
Initialization,
Execution,
Persistence.

That assumption is false for a request contract.

## D36_C quotient

The 36 MT cells collapse to five material invariants.

1. OBJECT_KIND precedes obligation selection.
2. UNIVERSAL portability coordinates must be separated from KIND-SPECIFIC coordinates.
3. NOT_APPLICABLE requires a typed witness; absence is not non-applicability.
4. A fresh-machine proof needs an EFFECTIVE REALIZER witness, not only semantic prose.
5. Self-application requires an anti-regress realization that does not depend on the
   repository whose portability is being tested.

## Tool Conductor result

ToolConductor was used as exhaustive repertoire coverage rather than as a selector.

Its current portable mathematics is:

TC_I(x,c)=(T~_i(x,c))_(i in I).

Every registered tool receives one conductor-level disposition. OPEN/BLOCKED remain
first-class.

For this repair, ToolConductor contributes two material checks:

A. SHOW_ME_THE_MATH must not invent itself as a configured tool merely to satisfy a
   tool-shaped checker.

B. Cross-machine portability of this one target depends only on its transitive
   load-bearing dependency cone, not on portable closure of every tool in MATERIAL_TOOLS.

Therefore ToolConductor's own global portability OPEN set does not block the local
SHOW_ME_THE_MATH self-hosting proof.

## Reconstructed generic math

For object X with kind kappa and package P:

LB(P,X)=mu S.(Roots(P,X) union Union_(s in S) Dependencies_P(s)).

DefinitionClosed(P,X,E)
iff every s in LB(P,X) is package-defined or a typed available primitive.

ObligationClosed(P,kappa)
iff every o in Req(kappa) is SATISFIED or NOT_APPLICABLE with witness.

ShowMathComplete_(J,K)(P,X;E)
iff
DefinitionClosed(P,X,E)
and ObligationClosed(P,Kind(X))
and RealizerAvailable(P,E)
and ProtectedEquivalent_(J,K)(Instantiate(P,E),X).

SMTM_(J,K)(P,X,E)
=
GREEN when ShowMathComplete_(J,K)(P,X;E),
RED(Residuals(P,X,E)) otherwise.

## REQUEST_CONTRACT specialization

Req(REQUEST_CONTRACT)
=
{Recognition,Evaluation,Projection}.

Persistence and configured-tool RunSpec are not constitutive requirements for this kind.
When mentioned, their non-applicability must have witnesses.

## Effective fresh-environment witness

runtime/show_me_the_math_portable.py

is a standalone standard-library-only realization.

The validation witness copies exactly this file to a new temporary directory and runs it
as a new Python process.

Required external primitive:

CPython 3.12+ standard library.

Repository access: false.
Conversation history: false.

## MT disposition

The previous RED self-application is explained by an over-broad obligation type.

The repaired mathematics has a concrete path to GREEN self-application without weakening
fail-closed recursive dependency closure.
