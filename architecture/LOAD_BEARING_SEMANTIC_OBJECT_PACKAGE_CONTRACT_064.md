# Load-Bearing Semantic Object Package Contract 064

Date: 2026-09-25
Status: CURRENT WORKING DESIGN CANDIDATE

## Problem

The system repeatedly discovers a load-bearing term, uses it in reasoning, and later loses its exact meaning because durable semantic capture is optional or fragmented.

Historical Black Box Registry and Semantic Preflight already established the key law:

an unresolved load-bearing primitive is legal;
silent use of it as though solved is not.

The missing step is lifecycle enforcement.

## Short-fix invariant

For every detected load-bearing semantic object o:

LoadBearing(o)
=>
Exists(DurablePackage(o))
OR
Closure = OPEN.

A package may contain unresolved content. Absence of solved mathematics does not block package creation.

Unresolved coordinates are recorded as BLACK_BOX_OPEN.

## MT dual output

MT has two distinct jobs:

1. transformation sensitivity

MT_sens(x)
=
systematically vary load-bearing coordinates of x
and return which variations change the protected result.

2. semantic capture obligations

MT_cap(x)
=
{ o | o is load-bearing in the MT run and lacks current durable semantic coverage }.

Configured MT closure requires every o in MT_cap(x) to receive a durable package or an explicit typed blocker.

MT does not have to solve every object it discovers.

## Package shape

Each semantic object receives:

- CORE.md — identity, type, current definition, known constraints, OPEN coordinates, dependencies, protected uses.
- MANIFEST.md — package status and document inventory.
- 36 directed scope-transition pages generated from the canonical six-scope ontology.

The 36 pages are not 36 meanings.
They are the 6 x 6 source-scope -> target-scope surface already recovered in the historical tool-family architecture.

Each transition page records:
- source scope
- target scope
- handoff type
- current disposition
- evidence
- OPEN coordinates
- affected uses

Unknown cell semantics are written as OPEN rather than omitted.

## Non-overwrite rule

New information does not silently replace prior semantic evidence.

Evidence is added as immutable evidence entries with unique IDs.
A later canonical summary may supersede an earlier summary only with explicit lineage.

CORE.md is a current projection over the retained evidence history, not the history itself.

## Black box

BLACK_BOX_OPEN(o)
iff
LoadBearing(o)
AND at least one semantic coordinate required by a current use remains unresolved.

BLACK_BOX_OPEN is not failure.
It is durable unresolved semantics.

## Tool

Bare "tool" is an umbrella label, not one semantic type.

Current required discrimination includes at least:
- question family
- semantic operator
- capability
- configured program
- controller
- wrapper
- runtime mechanism

Any result-sensitive use of "tool" must bind the intended subtype or remain BLACK_BOX_OPEN.

## Short fix vs large backfill

Short fix:
- install package schema/generator;
- require capture obligation for newly detected load-bearing objects;
- seed BLACK_BOX and TOOL;
- preserve OPEN;
- prevent overwrite-by-replacement.

Large backfill:
- instantiate/repair packages for the existing tool population and other historical load-bearing objects;
- validate each 36-cell surface;
- recover richer specs where legacy records are compressed.

Backfill is explicit Work, not a precondition for using the short fix on new discoveries.
