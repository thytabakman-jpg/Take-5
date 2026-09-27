# Take-6 Compiled Source Frontier 007

Date: 2026-09-27
Status: STRUCTURAL FRONTIER CURRENT / BYTE INGESTION PENDING

## Trigger

PR #154 advanced the compiled frontier to snapshot 006 and also persisted one
ImprovementCore run receipt outside the successor-bootstrap subtree. That receipt is
inside the declared Take-5 predecessor migration scope, so the source frontier
correctly reopened after the merge.

Snapshot 007 binds:

Commit:
91cc65b5379b9354036254c5dcff24d08490ae87

Tree:
55cc51cf22363e458c7f5f234109241e193cc16b

Take-5 in-scope entries:
931

Take-5 in-scope blobs:
884

## Delta inventory

Snapshot 007 derives the effective inventory from the frozen snapshot-004 full
inventory plus cumulative delta 007.

Delta 007 retains every snapshot-006 upsert and adds the durable ImprovementCore
run receipt introduced by PR #154.

## Current frontier size

Across Reaserch, Take-2, Take-3, Take-4, and Take-5 snapshot 007:

Tree entries:
3425

Git blobs:
3245

These 3,245 blobs are the current byte-ingestion target.

## Self-reference closure

This snapshot repair itself changes only take6-bootstrap/**, which is explicitly
outside the Take-5 predecessor migration scope while Take-6 is incubated inside
Take-5.

Therefore merging this repair does not create another predecessor-scope delta.

## Boundary

Structural frontier currentness does not imply byte ingestion, semantic
reconstruction, tool-capsule equivalence, disaster durability, or Take-6 promotion.
