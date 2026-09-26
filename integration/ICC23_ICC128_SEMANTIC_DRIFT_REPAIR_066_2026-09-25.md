# ICC-23 / ICC-128 Semantic Drift Repair 066

Date: 2026-09-25
Status: SHORT FIX IMPLEMENTED / HISTORICAL BACKFILL OPEN
Controllers: IC-023 observer/runtime-successor lens; ICC-128 closure owner

## Recovered user problem

The recurring failure was not merely missing definitions.

The system could:
1. introduce a load-bearing term/tool/object;
2. use it in later reasoning;
3. fail to create a durable exact semantic representation;
4. later reconstruct it differently or forget which unresolved coordinates mattered.

This produced repeated drift around words such as tool, black box, OPEN, sufficient, important, meaningful, and ICC itself.

It also forced the user to spend time reconstructing system semantics rather than using ASSERT and the rest of the tool system.

## Historical solution recovered

Reaserch already contained:
- Semantic Preflight;
- Black Box Registry;
- BLACK_BOX_OPEN;
- Artifact Reality;
- MT load-bearing-word artifact-reality audit;
- 36-cell tool-family surface;
- artifact-without-system-integration diagnosis.

The design was not lost conceptually. It was lost as a mandatory lifecycle invariant.

## PD / MT / ASSERT result

PD:
- discovered semantic object != deliberately created tool;
- unresolved discovered object may remain BLACK_BOX_OPEN;
- created tool cannot advertise a job while required mathematics for that job remains a hidden black box;
- one semantic object != 36 meanings;
- 36 pages are directed source-scope -> target-scope positions.

MT:
- MT has two outputs:
  1. transformation/result sensitivity;
  2. semantic capture obligations for newly exposed load-bearing objects.

ASSERT:
- optional capture is insufficient;
- advisory Jane alerts alone are insufficient;
- durable package existence must participate in admission;
- unknown load-bearingness cannot default to omission.

## Current short fix

### Durable package

Every captured semantic object receives:
- CORE.md;
- MANIFEST.md;
- 36 directed transition pages;
- append-only evidence entries.

Unknown cells are explicit OPEN.

### Jane

Jane owns lifecycle supervision:
- detect/receive load-bearing candidates;
- create capture work;
- keep package/currentness debt visible;
- trigger reentry.

Jane does not replace the mathematical solver/controller.

Unknown load-bearingness defaults to capture candidate, preventing silent false negatives.

### Emergent admission

A novel load-bearing object without a current semantic package remains OPEN.
Known-equivalent objects may MERGE without duplicating packages.

### Deliberately created tools/programs

CapabilityFoundry cannot return ADMISSION_REQUEST unless:
- semantic object identity exists;
- mathematical basis exists;
- required math coordinates are declared;
- every required coordinate is recovered;
- semantic package is current.

Thus a newly invented tool cannot enter the system with a hidden required mathematical black box.

### Seeded packages

- TERM:BLACK_BOX
- TERM:TOOL
- TERM:LOAD_BEARING
- OBJECT:SEMANTIC_PACKAGE

Each has CORE + MANIFEST + 36 transition pages.

## Tool distinction recovered

Bare TOOL is an umbrella term, not one type.

At minimum distinguish:
- question family;
- semantic operator;
- capability;
- configured program;
- controller;
- wrapper;
- runtime mechanism.

Result-sensitive use of bare "tool" remains semantically unsafe until subtype is bound.

## Short fix / large fix boundary

Short fix is prospective and now enforceable.

Historical tool/package debt remains real.
It is recorded in:
integration/SEMANTIC_PACKAGE_BACKFILL_001_2026-09-25.md

Backfill does not block use of the prospective invariant.

## Closure predicate

SHORT_FIX_CLOSED
iff
  package generator exists
  AND evidence overwrite is prohibited
  AND Jane emits mandatory capture work
  AND uncertain load-bearingness is not silently pruned
  AND novel load-bearing admission requires package coverage
  AND new tool/program admission requires complete-for-use mathematics plus package
  AND regression suite passes.

FULL_BACKFILL_CLOSED remains OPEN until all current material historical objects/tools have a current package or typed supersession/merge disposition.
