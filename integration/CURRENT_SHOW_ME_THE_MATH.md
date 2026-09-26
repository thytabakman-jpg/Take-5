# CURRENT SHOW ME THE MATH — Recovery Anchor 001

Date: 2026-09-26
Status: TAKE-5 CURRENT RECOVERY AUTHORITY
Canonical repository: thytabakman-jpg/Take-5

## Meaning

When the user says "show me the math", the default target is not a pretty equation
or a prose description.

The target is the complete portable reconstructive mathematics for the named formal
object, relative to the declared job and typed external environment.

Canonical condition:

ShowMathComplete_(J,K)(Package,T;E0)

iff the load-bearing symbol graph is recursively closed, initialization is executable,
runtime primitives are explicitly typed and available, persistence is specified, and
a fresh instantiation preserves the protected behavior of T.

## Fresh-environment test

fresh environment
+ PortableMath_(J,K)(T;E0)
-> T'

with

T' equiv_(J,K,Protected) T.

The fresh environment is assumed to have no conversation history and no Take-5/Reaserch
repository knowledge unless a repository is explicitly included as an external primitive.

## Fail-closed rule

For this job, a load-bearing symbol is GREEN only when its complete recursive meaning
is available from the supplied package or an explicitly typed primitive.

Otherwise it is RED/OPEN.

A familiar label, confidence, prior conversation, repository pointer, or named tool is
not enough.

## Response behavior

Default response:
1. mathematics first;
2. actual operators, relations, state, transitions and closure;
3. recursively expose load-bearing definitions;
4. expose typed primitives;
5. expose missing definitions/dependencies in RED;
6. do not silently borrow hidden context;
7. distinguish reconstructed math from runtime executability.

When the user asks for only the equation, keep the surface compact but do not color a
symbol green when its recursive mathematics is not available.

## Canonical files

Formal contract:
architecture/FULL_TOOL_MATHEMATICAL_IDENTITY_CONTRACT_002_2026-09-26.md

MT audit:
research/MT_SHOW_ME_THE_MATH_PORTABILITY_AUDIT_001_2026-09-26.md

Runtime policy:
runtime/show_me_the_math_contract.py

Tests:
tests/test_show_me_the_math_contract.py

Color integration:
integration/CURRENT_MATHEMATICAL_COLORING.md

## Object classification

SHOW_ME_THE_MATH is a request/job contract.
It is not a newly minted formal tool.
It does not replace MT, GOAL, ICC, Tool Conductor, or ImproveCore.

## Host boundary

Take-5 can enforce this contract only on execution/emission paths that load Take-5.
An unrelated host that never consults Take-5 remains an external host boundary.
