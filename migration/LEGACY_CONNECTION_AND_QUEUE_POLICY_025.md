# Legacy Connection and Work Queue Migration Policy 025

Date 2026-09-24
Scope Take-5 migration preparation
Authority nonproduction

## Decision

Take-5 must not have runtime dependencies on Take-2, Take-3, Take-4, or Reaserch.

Those repositories are frozen evidence/baseline sources during migration and rollback.

Connections are typed evidence relations, not live imports:
- RECONSTRUCTS_FROM
- BENCHMARKED_AGAINST
- PROVENANCE_FROM
- SUPERSEDES_AFTER_PROMOTION
- ROLLBACK_BASELINE

No legacy repository may be required for Take-5 ordinary runtime operation.

## Take-2

Preserve its important behavior, especially first-class Relation and the principle that backlog/debt/workstreams/transfer queues begin as views unless a separate durable surface demonstrates strict gain.

Do not connect Take-5 to Take-2 as a runtime dependency.

## Take-3

Preserve Take-3 as clean-room benchmark evidence. Its value depends on architectural independence, so connecting Take-5 runtime to it would damage the experiment.

Do not connect Take-5 to Take-3 as a runtime dependency.

## Take-4

Preserve as predecessor execution/control evidence and benchmark source. No runtime dependency.

## Reaserch

Remains production authority until promotion. During migration it is read-only baseline/rollback authority. It is not deleted or overwritten.

## Backlog and related queues

Do not copy BACKLOG.yaml, DEBT_REGISTER.yaml, WORKSTREAMS.yaml, SORT_LATER.yaml, or CROSS_PROJECT_TRANSFER_QUEUE.yaml as five independent architectural primitives.

Migrate their semantics into typed Work/Relation/State views:
BACKLOG -> inactive candidate Work objects
DEBT -> accepted-requirement deviation Work objects with cost/risk relation
WORKSTREAM -> active licensed Work view
SORT_LATER -> unresolved-routing Work objects
TRANSFER_QUEUE -> candidate transfer Relation/Work objects

Preserve the old invariants:
presence does not authorize execution;
file order does not establish priority;
OPEN/incomparability survive;
activation is an authority-bearing transition;
provenance survives.

Dedicated storage surfaces can be reintroduced only when a view/composition fails a result-sensitive requirement.

## Rollback

Promotion is reversible during confirmation:
1 Reaserch remains intact.
2 Take-5 receives copied/migrated state and evidence.
3 matched operation runs against frozen baseline.
4 production authority changes only after verification.
5 rollback restores prior authority pointer without reconstructing deleted data.

Destructive cleanup is a later independent operation, never part of initial promotion.
