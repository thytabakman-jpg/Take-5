# ImprovementCore Concurrency Preflight 084

Date: 2026-09-26
Status: ISOLATED STRICT-GAIN CANDIDATE / NOT CURRENT / NOT PROMOTED

## Problem

The ImprovementCore concurrency protocol already requires immutable workstream
records, explicit read/write sets, compare-and-swap shared writes, and
reconciliation rather than last-writer-wins.

Take-5 did not yet have an executable preflight that turns those declarations
into a fail-closed launch decision.

That leaves a gap between semantic concurrency policy and execution truth.

## Narrow improvement

Add a preflight relation over workstream footprints.

For workstream i let

R_i = declared read set
W_i = intended write set

For two active workstreams i and j define

Conf(i,j)
iff
W_i intersects (R_j union W_j)
or
W_j intersects (R_i union W_i).

The relation catches three distinct hazards:

1. proposed write invalidates another active reader;
2. concurrent write/write collision;
3. another active writer invalidates the proposed frozen read basis.

A launch is allowed only when:

- the active-workstream registry is declared complete for the checked scope;
- the proposed base snapshot is current;
- no active peer has Conf(i,j).

Otherwise the result is typed as BLOCK or RECONCILE_REQUIRED.

## Why this is a strict gain

Documentation already said concurrent ImproveCore work must not use
last-writer-wins. The new module makes that rule executable and testable.

It does not alter controller mathematics, currentness, HF routing, DCC closure,
or IC-031 successor semantics.

It therefore occupies a previously open realization gap rather than competing
with the active semantic successor work.

## Placement

Candidate runtime:
runtime/improvement_core_concurrency.py

Regression:
tests/test_improvement_core_concurrency.py

This candidate is deliberately not wired into the canonical dispatch in this
branch. Canonical activation requires reconciliation with every active
ImprovementCore workstream and a clean current-base comparison.

## Anti-collision rule for this branch

Write set is restricted to:

- runtime/improvement_core_concurrency.py
- tests/test_improvement_core_concurrency.py
- architecture/IMPROVEMENT_CORE_CONCURRENCY_PREFLIGHT_084.md
- integration/IMPROVEMENT_CORE_CONCURRENCY_WORKSTREAM_084.yaml

No current pointer, dispatcher, manager, IC-030/031 artifact, DCC artifact, HF
artifact, or shared registry is modified here.

## Remaining open

- authoritative discovery of all active workstreams across repositories;
- canonical dispatch activation;
- compare-and-swap enforcement at write time;
- automatic reconciliation scheduling;
- branch-lifetime and lease semantics;
- validation against live overlapping workstreams.

The candidate therefore improves collision detection without claiming universal
collision prevention.
