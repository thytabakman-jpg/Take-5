# Take-6 Bootstrap Validation 003

Date: 2026-09-27
Status: VALIDATED CANDIDATE / PRODUCTION PROMOTION OPEN
PR: #149

## Change under test

This validation replaces mutable predecessor-source currentness with a compiled
migration source frontier.

The repair adds:

- immutable repository source snapshots;
- explicit source-snapshot supersession;
- unique-maximal frontier compilation;
- OPEN/CONFLICT preservation;
- exact inventory binding;
- scope-aware Take-5 predecessor freshness while the successor is hosted inside Take-5;
- promotion blocking on an unverified source_frontier_cid;
- a non-authoritative BOOTSTRAP_MANIFEST projection.

## Live currentness exercise

The first candidate snapshot targeted Take-5 at:

a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2

During the run, Take-5 predecessor authority advanced in-scope to:

53b28a36d9998e4fe76f49b231695216fe419bdd

The gate detected the delta.

Snapshot 003 was appended rather than rewriting snapshot 002.

Snapshot 003 now compiles as the unique maximal Take-5 migration snapshot.

## Self-reference test

The declared predecessor scope excludes only:

- take6-bootstrap
- take6-bootstrap/**
- .github/workflows/take6-bootstrap-validation.yml

Regression coverage proves:

- successor-only hosted changes do not falsely stale the predecessor frontier;
- an in-scope Take-5 runtime change does stale the frontier;
- incomparable source snapshots compile to CONFLICT;
- unknown supersession fails closed;
- truncated source inventory fails closed.

## Validation evidence

Candidate head:
4ae35805aee600476f95243180b70f3beab38bbf

Take-6 Bootstrap Validation:
36294454479
SUCCESS
35 passed in 0.09s.

Capability Preservation:
36294454473
SUCCESS.

Live Take-5 predecessor authority during final frontier check:
53b28a36d9998e4fe76f49b231695216fe419bdd

## Disposition

Compiled source-frontier mechanism:
CLOSED_RELATIVE.

Current structural repository inventory:
PASS_RELATIVE_TO_SNAPSHOT_003.

Byte-level vault ingestion:
OPEN.

Semantic reconstruction:
OPEN.

Take-6 production promotion:
OPEN.

Take-5 remains current production authority.
