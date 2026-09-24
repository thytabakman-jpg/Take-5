# Improvement Core x Kernel Tool-Use Root Cause 001

Date: 2026-09-24
Status: ROOT-CAUSE FINDING / NONPRODUCTION REPAIR BASIS
Authority: successor-development only

## Symptom

Improvement Core repeatedly reasons about tools and capabilities without actually invoking the available repertoire as part of its own continuation.

## Root-cause chain

1. Historical IC had an explicit selection contract:
   cheapest capability or package that can change the live bottleneck;
   escalate only on residual interaction, noncommutation, or failed sufficiency;
   record material negative space;
   reselect on material delta.

2. Take-5 successfully compressed named tools into behavioral factors and the algebra
   T=<K,S,O,G,M,C,R,U>.

3. That compression preserved capability semantics but did not preserve the executable selector that turns a live blocker into a capability invocation.

4. ProgramRegistry stores capability metadata and executable status, but ProgramSpec has no trigger contract and the runtime has no general selector/dispatcher over the registry.

5. Only C01-C19 and C49 currently have executable adapters. C20-C48 are registered but not runtime-bound.

6. ICC_AUTONOMOUS_STEWARDSHIP says to use every useful capability, but this is prose-level policy. No state transition requires a capability-coverage disposition before IC can continue or claim closure.

Therefore the recurrent failure is not primarily reluctance, prompting, or insufficient intelligence. It is an architectural omission:

LIVE BOTTLENECK
  -/-> CAPABILITY COVERAGE
  -/-> SELECTED PROGRAM
  -/-> EXECUTION RECEIPT
  -/-> RESULT DELTA
  -/-> RESELECTION

## Minimal repair

Do not put tool choice inside K.

K owns the invariant that a material continuation or completion claim cannot silently bypass capability coverage.

R/controller owns selection.

Interface owns binding from selected semantic capability to an executable adapter.

Runtime owns execution.

State owns the coverage and execution receipts.

Verification owns the postcondition and reentry test.

## Required controller transition

BLOCKER
-> COVER_CAPABILITIES
-> {SELECTED, NO_APPLICABLE, UNBOUND, BLOCKED, OPEN}
-> EXECUTE_SELECTED where bound/licensed
-> RECORD_RECEIPT
-> VERIFY_EFFECT
-> REENTER

Every material capability in the current registry receives an explicit disposition. This preserves negative space and makes “did not use this tool” visible rather than silent.

## Kernel relation

Candidate kernel completion invariant:

A material continuation or completion claim is illegal when a capability that could materially change the live bottleneck has neither:
(a) an execution receipt, nor
(b) an explicit nonselection disposition with grounds.

This does not force ceremonial all-tool execution. It forces coverage.

## Important distinction

ALL-TOOLS AUDIT != EXECUTE EVERY TOOL.

The correct rule is:

For every registered capability, produce a relevance/binding disposition.
Execute every selected, bound, licensed capability needed to resolve the live bottleneck.
Escalate to packages only on residual interaction/noncommutation/failed sufficiency.

This reconstructs the exact old selection contract without reintroducing named-tool architecture as the primitive ontology.

## Current executable gap

C01-C19 and C49: runtime-bound in a5_programs.py.
C20-C48: semantic registry entries only.

Therefore current IC cannot literally execute the whole 49-capability repertoire.
Claiming otherwise would violate execution truth.

## Root disposition

ROOT_CAUSE = lost executable capability-selection/dispatch layer during behavior-first compression.

Contributing causes:
- registry metadata omitted executable trigger predicates;
- no generic dispatch contract;
- no coverage receipt;
- no kernel completion obligation requiring capability coverage;
- semantic “use tools” prose was mistaken for executable control;
- partial runtime binding was not propagated into IC stopping logic.
