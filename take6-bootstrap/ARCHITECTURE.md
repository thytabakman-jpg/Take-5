# Take-6 Architecture

## 1. Core model

Let the immutable evidence store be

[
V = \{(cid,x) : cid = H(x)\}.
]

Let the append-only event set be

[
E = \{e_1,e_2,\ldots\}
]

where every event is itself content-addressed and names its parents, subject, basis, authority, and effect.

The current semantic state is never authored. It is compiled:

[
S = C_\Sigma(V,E).
]

For a fixed schema/compiler version \(\Sigma\), compilation is deterministic:

[
(V,E,\Sigma)=(V',E',\Sigma')
\Rightarrow
C_\Sigma(V,E)=C_{\Sigma'}(V',E').
]

Any human-readable current page is a projection:

[
View = \pi(S)
]

and has no independent authority.

## 2. Currentness

For subject \(o\), let \(A_o\) be admitted versions and \(\succ\) the admitted supersession relation.

[
Current(o)=v
]

only when \(v\in A_o\) is the unique maximal admitted version.

If there are two incomparable maximal admitted versions:

[
Current(o)=CONFLICT.
]

If no adequate admitted version exists:

[
Current(o)=OPEN.
]

Recency alone never establishes currentness.

## 3. Compression safety

For a projection or compression \(q\) under job \(J\) and basis \(K\):

[
CompressionSafe_{J,K}(q)
\iff
\ker(q)\subseteq\equiv_{J,K}.
]

A projection without that witness may be displayed, indexed, or searched, but result-sensitive use requires rehydration from the exact source CIDs.

## 4. Tool identity

A configured tool is one immutable capsule:

[
T =
\langle
ID,
SpecCID,
RuntimeCID,
DependencyCIDs,
ProtectedBehavior,
EquivalenceTests,
EnvironmentContract
\rangle.
]

The authoritative tool identity is the capsule CID. Markdown names and aliases only resolve to that identity.

No second handwritten FullMath, registry, wrapper, runtime pointer, and current pointer are allowed to drift independently. They are either inside the capsule or generated from it.


## 4a. Specification before transformation

Immutable identity does not make an unknown object known.

For object \(o\), job \(J\), basis \(K\), and proposed transformation \(\tau\), let
\(Req_{J,K}(o,\tau)\) be the coordinates on which the protected result can depend.

A transformation is licensed only when every required coordinate is recovered or
has an admitted invariance witness proving that variation of the unresolved
coordinate cannot change the protected result.

\[
TransformLicensed_{J,K}(o,\tau)
\iff
Req_{J,K}(o,\tau)
\subseteq
Resolved_K(o) \cup Invariant_{J,K}(o,\tau).
\]

Object identity must also be IDENTIFIED, or the transformation must be invariant
across every surviving object hypothesis.

OBSERVE, DISCOVER, RECOVER, OBJECTIFY, FORMALIZE, COMPARE, AUDIT, VERIFY,
DIAGNOSE, and RECONSTRUCT remain legal on OPEN objects. Architecture, build,
modification, improvement, replacement, promotion, supersession, migration, and
other object-transforming transitions fail closed until this gate passes.

Package existence, content addressing, exact persistence, and runtime binding are
not substitutes for specification adequacy.

## 5. Invocation identity

Every execution uses:

[
I =
\langle
KernelCID,
StateCID,
ToolCID,
InputCIDs,
BasisCID,
EnvironmentCID
\rangle.
]

An invocation receipt records the exact capsule that ran.

A claim that a tool ran is invalid without an execution receipt whose invocation CID resolves.

## 6. Protected behavior preservation

For predecessor version \(v\) with protected behavior set \(P(v)\):

[
Promote(v\to v')
\Rightarrow
\forall b\in P(v),
Preserved(b,v,v')
\lor AuthorizedDelta(b)
\lor TypedOpen(b).
]

A missing behavior cannot disappear because the successor uses a different representation.

## 7. Affected-cone propagation

For material event \(e\), define:

[
Affected(e)
=
\mu X\left(
Seed(e)\cup Dependents(X)
\right).
]

Closure requires a typed disposition for every member of \(Affected(e)\).

This is the cross-project propagation mechanism. A mathematical discovery in one object is not considered integrated merely because it was written somewhere.

## 8. Archive

The vault stores exact bytes.

Each raw artifact record includes:

- SHA-256 CID
- original source and path
- byte count
- media type
- source repository/ref when applicable
- ingestion event
- extraction status
- duplicate-content relations
- provenance
- unresolved binary/encrypted status

Deduplication may collapse payload storage but never provenance.

## 9. Semantic extraction

Raw evidence never self-promotes.

Extraction creates candidate semantic objects.

Candidate semantic objects receive:
- stable identity
- type
- definitions
- dependencies
- protected behaviors
- OPEN coordinates
- provenance CIDs

Admission is a separate event.

## 10. Runtime

Runtime is replaceable.

A fresh runtime can reconstruct everything it needs from:
- kernel version
- compiled state
- exact tool capsule
- exact input objects
- explicit environment contract

Deleting the runtime cache or generated views cannot delete knowledge.

## 11. ImprovementCore placement

ImprovementCore is not the archive and not the kernel.

It is a controller package running above the kernel.

It may generate questions, select work, execute tools, learn, reenter, and propose new semantic objects.

It cannot:
- rewrite history;
- promote itself;
- manufacture currentness;
- bypass capsule identity;
- convert OPEN into PASS;
- make a generated view authoritative.

This restores the flexibility of the legacy controller while keeping persistence and authority outside the controller itself.

## 12. The anti-regression theorem target

For every protected object \(o\) and every admitted transition sequence \(\tau\):

[
Recoverable(o,\tau)
\lor
ExplicitlyUnresolved(o,\tau).
]

The forbidden state is silent semantic disappearance.

Take-6 is complete relative to a declared corpus only when no protected object reaches that forbidden state.
