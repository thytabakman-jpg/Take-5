# Take-6 Greenfield Bootstrap

Status: SUCCESSOR BOOTSTRAP CANDIDATE
Date: 2026-09-26
Source evidence: Reaserch, Take-2, Take-3, Take-4, Take-5, bound archives, current regression-permanence audit.

## Decision

Take-6 is not a rename of Take-5 and is not a bulk copy.

It is a clean successor architecture whose primary job is to make semantic loss, currentness drift, archive loss, wrapper loss, and capability regression structurally difficult.

The central design correction is:

authoritative history != compiled current state != runtime execution != human view.

Take-6 therefore separates three planes.

1. Evidence plane
   Immutable content-addressed raw objects plus an append-only event ledger.

2. Semantic plane
   A deterministic compiler derives the current object graph, current versions, dependency cones, OPEN/BLOCKED/CONFLICT state, tool capsules, and generated human views.

3. Execution plane
   A disposable runtime resolves exact content-addressed invocation capsules, executes them, emits receipts, and writes new evidence events. It never becomes the historical source of truth.

## Non-negotiable rule

No hand-authored CURRENT file, registry projection, summary, compressed view, or chat memory is authoritative.

All such surfaces are generated projections over immutable evidence and admitted events.

## Why this is a new system

Take-5 contains valuable safeguards and remains evidence. It also contains many independently maintained currentness, registry, recovery, manifest, architecture, and runtime surfaces. Synchronizing many authored projections recreates a drift surface.

Take-6 replaces synchronization-by-convention with compilation-from-events.

## Initial repository layout

```
vault/
  objects/sha256/
ledger/
  events/
schemas/
compiler/
runtime/
capsules/
compiled/          # generated, never authoritative
views/             # generated, never authoritative
migration/
tests/
```

## Authority order

1. byte identity in vault
2. admitted immutable ledger events
3. deterministic compiled semantic state
4. exact invocation capsule and execution receipt
5. generated views

A lower layer cannot silently overwrite a higher layer.

## Host boundary

Take-6 cannot force an unrelated ChatGPT host to load Take-6. Universal host interception remains externally owned.

Take-6 can make every repository-aware entry fail closed when the bootstrap, current compiled state, or exact invocation capsule is absent.


## Generated current views

The architecture rule that human CURRENT pages are non-authoritative projections
now has an executable realization:

take6-bootstrap/runtime/views.py

Generated views bind the exact compiled state, compiler, authority policy,
subject, payload and claim scope. Stale or tampered views fail verification.
Authoritative formal current claims additionally require dependency and type
closure.

Take-6 changes are now protected by the dedicated workflow:

.github/workflows/take6-bootstrap-validation.yml

Validation receipt:

take6-bootstrap/VALIDATION_002.md

This does not promote Take-6. Take-5 remains current authority until the full
migration/promotion boundary closes.


## Compiled migration frontier

The migration source basis no longer depends on a hand-maintained CURRENT cutoff.

Immutable source snapshots are stored under:

take6-bootstrap/migration/source_snapshots/

and compiled by:

take6-bootstrap/runtime/source_frontier.py

The compiler resolves a unique maximal snapshot per predecessor repository and preserves OPEN/CONFLICT when no unique frontier exists.

Take-5 predecessor freshness is scope-aware while the successor bootstrap is hosted inside Take-5. Changes under the successor-bootstrap subtree do not create self-referential lag; changes to the actual Take-5 predecessor runtime/architecture do.

Take-6 promotion now requires a verified source_frontier_cid.
