# Portable Mathematical Object Contract 001

Date: 2026-09-26
Status: CURRENT CANDIDATE / SELF-HOSTING TARGET
Canonical repository: thytabakman-jpg/Take-5

## Problem

The first SHOW_ME_THE_MATH contract inherited tool-shaped obligations from FullMath.
That is invalid for self-application because SHOW_ME_THE_MATH is a request contract,
not a configured tool.

The repair separates universal portability mathematics from kind-specific obligations.

## Generic object

Let X be a formal object with kind kappa.

P_X =
<
ObjectID,
Kind,
Signature,
Definitions,
LoadBearingSymbols,
RuntimePrimitives,
Obligations,
ProtectedBehavior,
EquivalenceTests,
Realizer,
EnvironmentContract
>.

The package may contain additional kind-specific coordinates.

## Recursive closure

LB(P,X)
=
mu S .
(
Roots(P,X)
union
Union_(s in S) Dependencies_P(s)
).

DefinitionClosed(P,X,E)
iff
for every s in LB(P,X),

Defined_P(s)
or
(
TypedPrimitive_P(s)
and
Available_E(Provider_P(s))
).

## Kind-indexed obligations

Let Req(kappa) be the required obligations for object kind kappa.

ObligationClosed(P,kappa)
iff
for every o in Req(kappa),

Satisfied_P(o)
or
(
NotApplicable_P(o)
and
Witness_P(o)
).

Current request-contract obligations:

Req(REQUEST_CONTRACT)
=
{Recognition,Evaluation,Projection}.

Therefore a request contract does not fail merely because it has no configured-tool
RunSpec or cross-run persistent memory.

Current tool obligations remain:

Req(TOOL)
=
{RunSpec,Initialization,Execution,Persistence}.

## Portability

RealizerAvailable(P,E)
means the package supplies an effective realization and every external evaluator/runtime
primitive is explicitly typed by E.

Let

X' = Instantiate(P,E).

ProtectedEquivalent_(J,K)(X',X)

holds when the declared protected observables agree under the supplied equivalence tests.

Then:

ShowMathComplete_(J,K)(P,X;E)
iff
DefinitionClosed(P,X,E)
and
ObligationClosed(P,Kind(X))
and
RealizerAvailable(P,E)
and
ProtectedEquivalent_(J,K)(Instantiate(P,E),X).

## Show-me-the-math operator

Residuals(P,X,E)
=
MissingFields
union UnresolvedSymbols
union UnavailablePrimitives
union UnsatisfiedObligations
union RealizerErrors
union EquivalenceErrors.

SMTM_(J,K)(P,X,E)
=
GREEN
when ShowMathComplete_(J,K)(P,X;E),

and

SMTM_(J,K)(P,X,E)
=
RED(Residuals(P,X,E))

otherwise.

## Self application

Let S denote SHOW_ME_THE_MATH and P_S its standalone package.

Kind(S)=REQUEST_CONTRACT.

Req(Kind(S))
=
{Recognition,Evaluation,Projection}.

The standalone realization is:

runtime/show_me_the_math_portable.py

Its only external evaluator is typed as:

CPYTHON_STDLIB_3_12.

The file contains the operator, closure algorithm, kind obligations, SELF_PACKAGE,
SELF_ENVIRONMENT and executable self-test.

No Take-5 import, repository fetch, or conversation state is required.

Self-hosting success criterion:

SMTM(P_S,S,E_python)=GREEN.

The CI regression test copies only that one file to an isolated temporary directory and
executes it with Python. This is the current effective fresh-environment witness.

## Relation to tool FullMath

For Kind(X)=TOOL, the existing:

FullMath_(J,K)(X)=<N_X,W_X,G_X,P_X,L_X>

and

RunSpec_K(X)=<X,W_X,G_X,R_X,C_X,H_X>

remain required coordinates of the tool package.

The generic object contract is not a replacement for FullMath. It is the portability
envelope within which FullMath is one kind-specific specialization.
