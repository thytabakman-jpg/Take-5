# Take-6 Compiled Source Frontier 002

Date: 2026-09-27
Status: IMPLEMENTED CANDIDATE / VALIDATION PENDING

## Problem found by ImprovementCore

The Take-6 migration source freeze still treated one hand-authored manifest entry as the effective Take-5 migration cutoff.

That cutoff was:

853c7f92dae62747d3f8f42a38b6d4b77e194ad2

After the formal-authority and generated-view repairs, Take-5 current authority had advanced to:

a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2

Git comparison showed:

- 47 commits ahead of the frozen migration cutoff;
- 70 changed files;
- material changes in runtime, architecture, integration, tests, ImprovementCore, mathematical coloring, formal-claim admission, and Take-6 successor work.

Therefore a successor built from the old cutoff could correctly compile a stale predecessor model.

Advancing the one cutoff field again would only recreate the same manual-currentness failure.

## Repair

Source currentness is now compiled from immutable snapshot history.

Runtime:

take6-bootstrap/runtime/source_frontier.py

Schema:

take6-bootstrap/schemas/source-snapshot.schema.json

Immutable snapshot evidence:

take6-bootstrap/migration/source_snapshots/REPOSITORY_SNAPSHOTS_001.json

take6-bootstrap/migration/source_snapshots/TAKE5_SNAPSHOT_002.json

Historical SOURCE_MANIFEST_001 remains evidence. It no longer owns migration-current source authority.

## Take-5 snapshot 002

Repository:

thytabakman-jpg/Take-5

Commit:

a773ac5ac00fe4d04bd8e22a3d0ae949a6f35af2

Tree:

104d50432a0aead4508890ef1a410fa7356e41c4

Inventory:

take6-bootstrap/migration/inventories/TAKE5_TREE_INVENTORY_002.json

Entries:

905

Blobs:

859

Recursive tree truncated:

false

It explicitly supersedes the historical migration snapshot at 853c7f92dae62747d3f8f42a38b6d4b77e194ad2.

## Self-reference resolution

Take-6 is temporarily hosted inside Take-5.

Raw Take-5 HEAD equality cannot be the migration freshness predicate because every successor-bootstrap edit would advance the host repository and make the predecessor snapshot instantly stale.

The new snapshot declares a predecessor scope excluding:

- take6-bootstrap
- take6-bootstrap/**
- .github/workflows/take6-bootstrap-validation.yml

Freshness for the Take-5 predecessor is therefore based on a deterministic digest of the in-scope Git inventory.

A successor-only host change does not reopen predecessor migration.

A changed in-scope Take-5 runtime, architecture, integration, protected behavior, or other predecessor object changes the digest and blocks promotion until a new immutable snapshot explicitly supersedes the old frontier.

## Compiled-current law

For each predecessor repository r, collect all admitted immutable source snapshots and their explicit supersession edges.

The unique non-superseded maximal snapshot is migration-current.

Two incomparable maxima compile to CONFLICT.

No maximal snapshot compiles to OPEN.

No branch label, timestamp, filename, or manifest position establishes migration currentness.

## Promotion consequence

Take-6 promotion now requires:

- compiled source frontier status CURRENT for required predecessor repositories;
- inventory verification;
- observed predecessor-scope digest match;
- a source_frontier_cid recorded in the promotion receipt.

Missing or stale frontier verification fails closed.

## Historical preservation

SOURCE_MANIFEST_001 and TAKE5_TREE_INVENTORY_001 are not overwritten or relabeled current.

They remain immutable evidence of the prior migration basis and the currentness failure that this repair addresses.
