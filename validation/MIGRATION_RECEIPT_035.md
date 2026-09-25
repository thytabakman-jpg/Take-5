# Migration Receipt 035

Date 2026-09-24
Status MIGRATED_WORKING
Authority Take-5 canonical working successor
Rollback baseline Reaserch preserved intact

## ImproveCore audit decision

GO after reconciliation and repair.

The apparent 4x4/6x6 conflict was not resolved by choosing four.
No canonical 4x4 claim was found.

Newest validated research supports:
1 Scope x ModeFace = 6x6 = 36 as ImproveCore controller coverage/routing/challenge/completion lattice.
2 SourceScope x TargetScope = 6x6 = 36 as a distinct directed handoff graph.

They are separate typed structures.
The earlier error was conflating equal-cardinality structures.

## Root-cause repair during migration

Final pre-promotion A5 run exposed one real RCDL bootstrap defect:
candidate generation on an empty prior view could index a missing view.

Root cause:
RCDL initialization assumed a prior generated representation.

Repair:
empty prior state now receives an explicit empty CandidateUniverse rather than executing view-dependent generators against a nonexistent view.

## Final executable evidence

A5 Tests run 36080072665 on commit f602a6c342730ef2d4e40e332cd0754637f1761e: PASS, 192 passed.
Closed Loop Fixture run 36080072677: PASS.
Dump Test run 36080072652: PASS.

## Migrated state

README now declares Take-5 CANONICAL_WORKING.
MIGRATION_STATE.yaml records user authorization, source heads, rollback and OPEN validation.
architecture/CANONICAL_FOUNDATION_034.md is the current foundation.
runtime/scope_mode_36.py implements the canonical controller 36 lattice.
The Reaserch cross-chat migration packet and IC-030 evidence are copied into Take-5 provenance.

## Preservation

Reaserch was not deleted, overwritten, archived, or destructively modified by this migration.
It remains the rollback/provenance baseline.

The migration does not claim every historical file has been physically duplicated.
The preserved repository remains authoritative provenance for historical material while backfill stays explicit.
No absence in Take-5 is interpreted as historical nonexistence.

## Operating transition

New work begins in Take-5.
New discoveries enter through currentness/admission and can trigger another rebase/migration.
Rollback can restore the Reaserch authority pointer without reconstructing deleted data.

## Result

MIGRATION GO executed.
TAKE-5 is the go-to canonical working system.
