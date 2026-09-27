# Take-6 Migration Strategy

Status: GREENFIELD MIGRATION PLAN

## Principle

Do not copy Take-5 into Take-6 and call it a successor.

Take-5 is evidence.

The migration unit is:

[
M =
\langle
Evidence,
Identity,
Semantics,
Authority,
ProtectedBehavior,
RuntimeBinding,
State,
Provenance,
Disposition
\rangle.
]

## Phase 1: freeze sources

Bind exact refs for:
- Reaserch
- Take-2
- Take-3
- Take-4
- Take-5
- the historical ICC128 Legacy snapshot
- every available bound ZIP/archive
- current conversation/export evidence when available

Record immutable source snapshots with repository, exact commit, exact tree, inventory, scope, and explicit supersession.

Compile the active migration frontier from all admitted snapshots. No single manifest path or branch label is a CURRENT pointer.

While the Take-6 bootstrap is temporarily hosted inside Take-5, the declared predecessor scope excludes the successor-bootstrap subtree and its dedicated validation workflow. This prevents successor-only commits from creating self-referential migration lag while preserving sensitivity to real Take-5 runtime, architecture, and protected-behavior changes.

### Phase 1 closure law

For predecessor repository r with compiled frontier F_r and observed authority surface O_r:

[
SourceFrontierClosed(r)
\iff
Status(F_r)=CURRENT
\land
ScopedDigest(F_r)=ScopedDigest(O_r).
]

Raw HEAD equality is not required when the difference is entirely outside the declared predecessor migration scope.

A real in-scope predecessor delta reopens migration and blocks promotion until a new immutable snapshot explicitly supersedes the prior frontier.

## Phase 2: ingest

Ingest exact bytes into the vault.

No semantic decision occurs during byte ingestion.

Every member receives:
- CID
- source locator
- source version
- byte count
- media type
- extraction disposition

Unreadable/binary/encrypted evidence remains explicit.

## Phase 3: reconstruct semantic objects

Extract candidates for:
- ideas
- distinctions
- equations
- tools
- wrappers
- controllers
- runtime mechanisms
- project state
- decisions
- rejected alternatives
- failures
- benchmarks
- OPEN questions

Every candidate points back to exact evidence CIDs.

## Phase 4: unify identities

Do not merge by name.

Use explicit equivalence/supersession evidence.

Aliases, versions, capabilities, packages, controllers, and runtimes remain distinct object kinds.

## Phase 5: admit current semantic state

For each subject, compile:
- CURRENT
- HISTORICAL
- SUPERSEDED
- REJECTED
- OPEN
- BLOCKED
- CONFLICT

No hand-authored CURRENT table is migrated as authority.

## Phase 6: compile tool capsules

Every operational tool receives one content-addressed capsule containing:
- exact mathematical/semantic specification
- configured wrapper
- scope geometry
- recurrence/HF rules
- dependencies
- runtime binding
- environment contract
- protected behaviors
- regression/equivalence tests

Missing coordinates remain OPEN and prevent full operational promotion.

## Phase 7: differential behavioral validation

For each predecessor protected capability:

[
Pres_{old}(c)
\Rightarrow
Pres_{new}(c)
\lor StrictGainReplacement(c)
\lor AuthorizedSupersession(c)
\lor OPEN(c).
]

Run historical and prospective holdouts.

Legacy ImprovementCore is a protected behavioral benchmark, not a codebase to copy.

## Phase 8: switch authority

Take-6 becomes runtime authority only after:
- migration corpus accounting passes;
- current compiler determinism passes;
- tool capsule resolution passes;
- protected behavior preservation passes;
- cross-project affected-cone closure passes;
- runtime execution receipts pass;
- recovery from a fresh checkout passes.

Until then Take-5 remains the working authority.

## Phase 9: predecessor freeze

After promotion, predecessor repositories remain immutable provenance and fallback evidence.

Do not delete them.
