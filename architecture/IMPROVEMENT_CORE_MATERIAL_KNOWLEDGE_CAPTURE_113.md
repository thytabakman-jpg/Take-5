# ImprovementCore Material Knowledge Capture 113

Date: 2026-09-26
Status: CURRENT / VALIDATED / REPOSITORY-GOVERNED CLOSED_RELATIVE
Controller: ImprovementCore
Canonical repository: thytabakman-jpg/Take-5

## Problem

The system had several anti-loss mechanisms:

- MAP_CAPTURE_POLICY.md;
- Functionality Recovery Ledger;
- cross-chat integration capture;
- durable negative-route learning;
- protected-transition integrity;
- provenance/currentness/reentry rules.

Those mechanisms did not yet establish one mandatory runtime transition from a material
ImprovementCore discovery to durable integrated knowledge.

Therefore this stronger claim was false:

Every material idea discovered during governed ImprovementCore execution is durably recorded,
connected to provenance/dependencies, and recoverable after the episode.

The missing generator was:

MATERIAL_DISCOVERY
!=>
MANDATORY_DURABLE_KNOWLEDGE_INTEGRATION.

## Repair

New runtime:

runtime/improvement_core_knowledge_ledger.py

New durable ledger:

integration/IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json

The current ImprovementCore regime now loads the ledger and captures two classes.

### Explicit knowledge events

A stage may emit:

knowledge_events = [
  {
    kind,
    statement,
    basis_id,
    source_route,
    disposition,
    related_objects,
    dependency_footprint,
    evidence_refs,
    metadata
  }
].

Every explicit event crossing the regime is persisted.

### Recursive material transitions

The recursive parent manager already emits traces containing selected job, admitted delta,
and progress effects.

The regime now converts material recursive traces into durable MATERIAL_TRANSITION nodes.

This prevents a strict-gain discovery from existing only in transient parent/child state.

## Knowledge object

A durable node contains:

K
=
<
  KnowledgeID,
  Kind,
  Statement,
  Basis,
  Disposition,
  RelatedObjects,
  DependencyFootprint,
  EvidenceRefs,
  Provenance,
  Metadata
>.

The ledger also retains an append-only history of capture/integration transitions.

## Anti-loss law

Let M(e) mean that event e is emitted as an explicit knowledge event or appears in an admitted
recursive trace with a material delta/progress effect.

Let P(e) mean that the knowledge ledger contains a durable node for e and a provenance history
entry.

Repository-governed capture invariant:

forall e,
M(e)
=>
P(e).

Repeated capture integrates provenance/evidence into the same knowledge node rather than creating
a duplicate node.

Rejection or supersession changes disposition. It never deletes historical capture.

## Authority law

Captured(e)
does not imply
Admitted(e).

Admitted(e)
does not imply
Current(e).

The ledger is an anti-loss and integration spine, not an authority shortcut.

## Integration law

Each knowledge node can carry:

- related formal/system objects;
- dependency footprint;
- evidence references;
- multiple provenance records;
- typed disposition.

This supplies the minimum machine-readable graph needed to connect an idea to the objects that
can be invalidated, reopened, superseded, or recovered later.

## Distinction from durable negative learning

integration/IMPROVEMENT_CORE_DURABLE_LEARNING_110.json stores certified route outcomes used to
block unchanged NO_GAIN/REJECTED/FAILED/CYCLE routes.

integration/IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json stores material knowledge.

Both are required.

Negative route memory answers:

What work have we learned not to repeat unchanged?

Knowledge memory answers:

What material idea/relation/distinction/problem/solution did we discover and how is it connected?

## Scope boundary

This closes only repository-governed ImprovementCore capture.

It does not imply that Take-5 can enumerate or capture:
- chats the host never exposes;
- external files/sources never supplied;
- thoughts never emitted through a governed path;
- every future semantic implication of already-captured knowledge.

Therefore:

RepositoryGovernedMaterialCapture = CLOSED_RELATIVE.

UniversalRecordEverything = OPEN / EXTERNAL_NOT_OWNED where source events never enter the system.

## Validation requirements

1. explicit knowledge event survives a fresh process;
2. recursive material transition is auto-captured;
3. duplicate capture integrates rather than duplicates;
4. supersession/rejection preserves historical node and history;
5. unresolved CAPTURED/OPEN/BLOCKED/CONFLICT nodes remain queryable;
6. full Take-5 validation passes;
7. Capability Preservation passes.

## Result

The prior problem "we record many things but a material idea can still fall between chat/run and
the durable system" has a direct runtime repair.

The stronger open-world claim "nothing anywhere can ever be lost" remains unlicensed.


## Validation evidence

PR #111
- merge: 4fcbb2ef98e830d648ff09c4630d3440b0c2a1fb
- Take-5 Validation: 36265770070 SUCCESS
- Capability Preservation: 36265770012 SUCCESS

The validation suite exercised explicit knowledge-event persistence, fresh-process reload,
duplicate integration, supersession preservation, unresolved querying, recursive material
transition capture, the full Take-5 suite, whole-system audit, closed-loop fixture, and
zero-request dump.
