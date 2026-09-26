# CURRENT SHOW ME THE MATH — Recovery Anchor 002

Date: 2026-09-26
Status: TAKE-5 CURRENT / SELF-HOSTING CANDIDATE
Canonical repository: thytabakman-jpg/Take-5

## Meaning

"Show me the math" means:

Recover and display the complete portable reconstructive mathematics of the target
formal object so that its protected behavior can be reconstructed in a fresh environment
without hidden conversation history or repository knowledge.

It is a request/job contract, not a configured tool.

## Generic object mathematics

For target object X, package P and environment E:

LB(P,X)
=
mu S .
(
Roots(P,X)
union
Union_(s in S) Dependencies_P(s)
).

DefinitionClosed(P,X,E)
iff every symbol in LB(P,X) is either package-defined or an explicitly typed primitive
whose provider is available in E.

Let Req(Kind(X)) be the obligations required by the mathematical species of X.

ObligationClosed(P,Kind(X))
iff every required obligation is either SATISFIED or NOT_APPLICABLE with a typed witness.

Then:

ShowMathComplete_(J,K)(P,X;E)
iff
DefinitionClosed(P,X,E)
and
ObligationClosed(P,Kind(X))
and
RealizerAvailable(P,E)
and
PortableEquivalent_(J,K)(Instantiate(P,E),X).

The user-visible operator is:

SMTM_(J,K)(P,X,E)
=
GREEN

when ShowMathComplete holds, and

SMTM_(J,K)(P,X,E)
=
RED(Residuals(P,X,E))

otherwise.

## Self application

Let S = SHOW_ME_THE_MATH.

Kind(S)=REQUEST_CONTRACT.

Req(REQUEST_CONTRACT)
=
{Recognition,Evaluation,Projection}.

Therefore S is not required to possess a configured-tool RunSpec or persistent controller
memory. Those coordinates are NOT_APPLICABLE only with explicit witnesses.

The standalone realization is:

runtime/show_me_the_math_portable.py

Its external environment contract is:

CPython 3.12+ standard library.

Repository access required: false.
Conversation history required: false.

The self-hosting success criterion is:

SMTM(P_S,S,E_python)=GREEN.

## Effective fresh-environment test

tests/test_show_me_the_math_self_hosting.py copies only
runtime/show_me_the_math_portable.py into an isolated temporary directory and executes
it as a new Python process.

The same regression also:
- runs the current MT semantic return gate on the repaired self-package and requires
  CLOSED_RELATIVE with no open objects;
- runs the current ToolConductor across the complete registered MATERIAL_TOOLS repertoire
  and requires exactly one conductor-level disposition per tool;
- preserves fail-closed RED behavior when a hidden dependency or required request-contract
  obligation is removed.

## Color rule

For this exact job:

GREEN_(showmath)(s)

iff s lies in a recursively closed dependency cone terminating only in supplied
definitions or explicitly typed available primitives and all kind-relevant portability
obligations are closed.

Otherwise:

RED_(showmath)(s).

A repository pointer, familiar name, remembered conversation meaning, or prose label
cannot promote a symbol.

## Canonical files

Generic portability contract:
architecture/PORTABLE_MATHEMATICAL_OBJECT_CONTRACT_001_2026-09-26.md

Tool specialization:
architecture/FULL_TOOL_MATHEMATICAL_IDENTITY_CONTRACT_002_2026-09-26.md

MT self-hosting repair:
research/MT_SHOW_ME_THE_MATH_SELF_HOSTING_002_2026-09-26.md

Standalone realization:
runtime/show_me_the_math_portable.py

Compatibility checker:
runtime/show_me_the_math_contract.py

Self-hosting regression:
tests/test_show_me_the_math_self_hosting.py

Color integration:
integration/CURRENT_MATHEMATICAL_COLORING.md

## Host boundary

The mathematical package is portable to a fresh Python environment.

Automatic interpretation of the phrase in a chat host that never loads the Take-5
contract remains an external host-routing boundary. That host boundary is not part of
the portability proof of the mathematical object itself.
