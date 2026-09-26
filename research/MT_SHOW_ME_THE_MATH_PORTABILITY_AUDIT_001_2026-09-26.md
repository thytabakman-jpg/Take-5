# MT — SHOW ME THE MATH portability audit 001

Date: 2026-09-26
Status: MATERIAL_YIELD
Canonical repository: thytabakman-jpg/Take-5
Target: the recovered user meaning of "show me the math"
Execution truth: HOST_BOUND_CONFIGURED / SEMANTICALLY_APPLIED
Configured tool: MT
Mode: OBSERVER
Geometry: D36_C = 6 scopes x 6 mode faces = 36 cells
Wrapper: canonical math-first configured MT wrapper

## Input claim

The target interpretation is stronger than displaying equations.

When the user says "show me the math", the intended job is:

Recover and display the complete load-bearing mathematical object such that a fresh
environment with no conversation history and no repository access can reconstruct the
same protected tool behavior from the supplied mathematical package plus explicitly
typed external primitives.

## 36-cell quotient

The 36 configured MT cells collapse to seven non-equivalent distinctions.

1. DISPLAYED_EQUATION != RECONSTRUCTIBLE_MATHEMATICAL_OBJECT
2. NAMED_SYMBOL != DEFINED_SYMBOL
3. SOURCE_RECOVERABLE != PACKAGE_SELF_CONTAINED
4. INTERFACE_SUFFICIENT != PORTABLE_IMPLEMENTATION_COMPLETE
5. HIDDEN_DEPENDENCY != TYPED_EXTERNAL_PRIMITIVE
6. SYNTACTIC_EQUALITY != PROTECTED_BEHAVIOR_EQUIVALENCE
7. SEMANTIC_RECOVERY != FRESH_ENVIRONMENT_INSTANTIABILITY

No cell supplies grounds for weakening any of these distinctions.

## Required new objects

ShowMathJob_(J,K)(T)
PortableMath_(J,K)(T;E0)
LoadBearingClosure_(J,K)(T)
FreshEnvironment E0
DefinitionClosure
Initialization witness
Runtime/primitive witness
ProtectedBehaviorEquivalence witness
HiddenDependency witness

## Core reconstruction

Base configured-tool identity remains:

FullMath_(J,K)(T)
=
<N_T,W_T,G_T,P_T,L_T>.

Concrete execution remains:

RunSpec_K(T)
=
<T,W_T,G_T,R_T,C_T,H_T>.

For the show-math job, define the load-bearing symbol closure as the least fixed set
containing every symbol used by FullMath and RunSpec and every symbol used recursively
by their definitions:

LB_(J,K)(T)
=
mu S . (
Symbols(FullMath_(J,K)(T),RunSpec_K(T))
union
Union_{s in S} Dependencies(s)
).

Let Package define symbols and let E0 expose explicitly typed external primitives.

DefinitionClosed_(J,K)(Package,E0,T)
iff
for every s in LB_(J,K)(T),
Defined_Package(s)
or
TypedPrimitive_E0(s).

A primitive is not licensed merely because a host happens to know it. Its type,
contract, and availability assumptions must be explicit.

Define the portable mathematical package:

PortableMath_(J,K)(T;E0)
=
<
FullMath_(J,K)(T),
RunSpec_K(T),
Definitions,
Initialization,
RuntimePrimitives,
Persistence,
ProtectedBehavior,
EquivalenceTests
>.

Instantiation target:

Instantiate(PortableMath_(J,K)(T;E0),E0)
=
T'.

The portability proof obligation is behavioral:

T' equiv_(J,K,Protected) T.

Therefore:

ShowMathComplete_(J,K)(T;E0)
iff
DefinitionClosed_(J,K)
and InitializationExecutable
and RuntimePrimitivesAvailable
and PersistenceSpecified
and ProtectedEquivalent(T',T).

## Color consequence

For the exact job SHOW_ME_THE_MATH:

GREEN_(J,showmath)(s)
iff
s is recursively closed relative to Package + typed E0 primitives and every
claim-relevant portability obligation is satisfied.

Otherwise RED_(J,showmath)(s).

A familiar name, repository pointer, prose role, confidence judgment, or historical
memory cannot promote a red symbol.

## Output consequence

"Show me the math" defaults to the actual mathematical object, not an explanatory essay.

The response must:
- emit the equations/relations/state/transition structure;
- recursively expose load-bearing definitions;
- expose external primitives as typed primitives;
- expose unresolved or hidden dependencies as RED/OPEN;
- not substitute labels for mathematics;
- not silently borrow conversation or repository memory;
- distinguish formal reconstruction from executable runtime availability.

## MT disposition

MATERIAL_YIELD.

The previous Take-5 contracts partially support this meaning:
- configured FullMath distinguishes native semantics, wrapper, geometry, proof, lineage;
- current coloring is job-relative and fail-closed;
- configured execution distinguishes selected, executed, captured, consumed.

Material missing pieces before this change:
- no canonical Take-5 "show me the math" request contract;
- no fresh-environment criterion;
- no recursive symbol-closure rule;
- no runtime enforcement surface for hidden dependencies;
- the historical Full Tool Mathematical Identity contract was not present at the expected Take-5 current path.

These are the repair targets of this change.
