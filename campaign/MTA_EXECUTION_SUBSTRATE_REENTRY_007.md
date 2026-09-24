# MTA REENTRY — EXECUTION SUBSTRATE AND ZERO-REQUEST SWEEP

Date 2026-09-24
Mode nonproduction
Migration prohibited

## MTA target
Observation: Reaserch Actions jobs are created but terminate in roughly 2–3 seconds with runner_id=0, empty runner_name, and steps=[].

## Differentiate
This is not evidence that repository tools fail.
It is pre-execution failure.

Execution coordinates must therefore be separated:

Selected(t)
Bound(t)
Schedulable(t)
RunnerAssigned(t)
Started(t)
Executed(t)
Succeeded(t)
Consumed(t)

ToolUse(t) requires at minimum Started AND Executed AND Receipt AND Consumed.
Workflow job existence is insufficient.

## Factor
Observed failure is upstream of repository code execution:
runner_id=0
runner_name empty
steps empty

Therefore current evidence localizes the defect to host scheduling/runner assignment or an equivalent pre-step workflow substrate boundary. Exact external cause remains OPEN because no runner-side logs exist.

## Reconstruct
The prior plan wrongly treated the GitHub Actions substrate as a transparent implementation detail.
Correct architecture requires an execution-substrate coordinate E and explicit realizability gate.

A program p is executable in environment e only when:
SemanticBinding(p) AND Authority(p,e) AND Dependencies(p,e) AND Schedulable(p,e).

Execution evidence requires:
Started(p,e) AND Receipt(p,e).

## Result sensitivity
Without this distinction the project can falsely infer capability failure from host failure and can falsely infer capability recovery from registration.

## Revised plan
1 Preserve host failure as typed EXTERNAL/PRE_EXECUTION OPEN, not tool FAIL.
2 Do not block semantic A5 construction on an unavailable host when independent implementation work is possible.
3 Continue family reconstruction locally at repository-artifact level with CI status OPEN until executable host evidence returns.
4 Retry zero-request full-repertoire execution when substrate becomes schedulable.
5 Maintain per-tool execution truth ledger so no tool receives credit without a receipt.
6 Architecture Analysis and MTA reenter after each family and after substrate recovery.
7 Migration remains prohibited.

## New architecture obligation
Extend realization semantics with execution environment E without automatically promoting E to a ninth semantic role:
Realizable(p,e)=Bound(p) AND Licensed(p,e) AND DepsAvailable(p,e) AND Schedulable(p,e).

Whether E belongs inside S/K or is an external environment coordinate remains OPEN and is an Architecture Analysis target.

## Improvement Core decision
Current best next work is parallel:
A. execution-substrate diagnosis/watch
B. continue A5 MAP implementation and tests
C. build execution-truth ledger
D. on host recovery, run zero-request repertoire sweep and consume results before readiness.

This dominates waiting idly for Actions and dominates pretending Actions ran.
