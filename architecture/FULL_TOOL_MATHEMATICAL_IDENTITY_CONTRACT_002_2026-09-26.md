# Full Tool Mathematical Identity Contract 002

Date: 2026-09-26
Status: TAKE-5 CURRENT / PORTABILITY-EXTENDED
Canonical repository: thytabakman-jpg/Take-5
Historical source:
thytabakman-jpg/Reaserch@e4c76c595b44a35fd9efc02cde8979e656ef54e8
projects/tool-lineage/FULL_TOOL_MATHEMATICAL_IDENTITY_CONTRACT_001_2026-09-26.md

## 1 Governing identity

For protected job J and basis K:

FullMath_(J,K)(T)
=
<N_T,W_T,G_T,P_T,L_T>.

A named tool is not mathematically recovered merely because one equation, one role,
or one runtime file is known.

## 2 Native semantics

N_T
=
<Type_T,Dom_T,Cod_T,State_T,Graph_T,Adm_T,Obs_T>.

## 3 Wrapper/execution identity

W_T
=
G_Tool(W^-_T,W^o_T,W^+_T,W^x_T).

W^-_T = PRE dependencies and entry gates.
W^o_T = INTRA-run controls/interleavings.
W^+_T = POST consequences, verification, closure, persistence and reentry.
W^x_T = CROSS-run/cross-tool/cross-scale dependencies and propagation.

Two tools with identical native semantics but materially different result-sensitive
wrappers are different configured tools.

## 4 Geometry identity

G_T
=
<Scope_T,Mode_T,Order_T,Arity_T,Representation_T,Scale_T,Coverage_T>.

Geometry is load-bearing whenever changing it changes protected discovery, routing,
evidence, reachable continuations, or output.

## 5 Protected behavior identity

P_T
=
<Protected_T,Witness_T,Regression_T,Closure_T,Counterexample_T>.

For every protected p:

Recover(CanonicalToolIdentity(T),p)=PASS

is required for full recovery relative to the declared job.

## 6 Lineage/currentness/reality identity

L_T
=
<Identity_T,Version_T,Lineage_T,Authority_T,Currentness_T,Runtime_T,
ExecutionTruth_T,Persistence_T,CanonicalRefs_T,Open_T>.

Recency is not authority.
Repository storage is not runtime execution evidence.
Persistence is a mathematical coordinate when it changes protected behavior.

## 7 Run specification

RunSpec_K(T)
=
<T,W_T,G_T,R_T,C_T,H_T>.

Missing a load-bearing invocation coordinate yields OPEN/BLOCKED rather than silent
downgrade.

## 8 Recovery criterion

Recovered_(J,K)(T)

requires N_T, W_T, G_T, P_T, L_T and all claim-relevant RunSpec coordinates to be
reconstructible, with unresolved coordinates explicitly typed OPEN/BLOCKED.

This is semantic/configured recovery. It is not yet the stronger portability claim.

## 9 Portability extension

For SHOW_ME_THE_MATH and any job explicitly requiring standalone reconstruction, define:

LB_(J,K)(T)
=
mu S . (
Symbols(FullMath_(J,K)(T),RunSpec_K(T))
union
Union_{s in S} Dependencies(s)
).

DefinitionClosed_(J,K)(Package,E0,T)
iff
for every s in LB_(J,K)(T),
Defined_Package(s)
or
TypedPrimitive_E0(s).

Define:

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

Instantiate(PortableMath_(J,K)(T;E0),E0)=T'.

PortableEquivalent_(J,K)(T',T)
iff
ProtectedObservables_(J,K)(T')
equiv
ProtectedObservables_(J,K)(T).

ShowMathComplete_(J,K)(T;E0)
iff
DefinitionClosed_(J,K)(Package,E0,T)
and InitializationExecutable
and RuntimePrimitivesAvailable
and PersistenceSpecified
and PortableEquivalent_(J,K)(T',T).

A source pointer is evidence/provenance, not a substitute for package closure.

## 10 Hidden-dependency rule

For the portability job, a load-bearing symbol is RED/OPEN whenever:
- its definition is absent;
- its dependencies are absent;
- it is only named;
- its meaning depends on conversation memory;
- its meaning depends on an unbundled repository artifact;
- an external primitive lacks a typed contract or availability assumption;
- initialization/runtime/persistence needed for protected behavior is missing.

## 11 Tool creation and successor gate

A new formal tool requires a canonical full-math artifact containing native math,
wrapper, geometry, protected behavior, lineage/currentness/runtime boundary,
closure/reentry, OPEN coordinates, and canonical identity.

A successor may supersede a predecessor only with explicit dispositions for protected
behavior and wrapper/geometry changes.

## 12 HF002 coordinate

Every named configured tool wrapper includes an HF002 applicability coordinate with
one typed disposition:
REQUIRED_BY_RULE, NOT_APPLICABLE with witness, OPEN with discriminator, or BLOCKED
with resume condition.

Actual recurrence remains conditional.

## 13 SHOW_ME_THE_MATH specialization

The phrase "show me the math", and close variants such as "show the full math",
"give me the actual math", or "show me the full math equation", select the portability
job unless the user explicitly narrows the request to a smaller projection.

This is a request contract, not a new formal tool identity.

The default user-visible projection is mathematics first. Prose is used only to type
unresolved coordinates, primitives, boundaries, or exact translations.

## 14 Nonclaims

This contract does not claim:
- literal LaTeX is directly executable;
- every external primitive can be eliminated;
- universal host interception;
- universal termination;
- every current Take-5 tool already passes ShowMathComplete.

It defines the target and fail-closed test.
