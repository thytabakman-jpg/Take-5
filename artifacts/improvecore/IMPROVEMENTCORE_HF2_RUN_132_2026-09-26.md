# ImprovementCore + HF2 Run 132 — 2026-09-26

## Invocation

User request:
"Run improvement core with an HF2."

Trigger commit:
0ff1a4648ca258f9e79508429680e2bf165bbf4a

Canonical execution workflow:
ImproveCore Self Study 104

Workflow run:
36278090571

Take-5 validation run:
36278090627

Both completed SUCCESS.

## Execution truth

The workflow executed:
runtime/improvement_core_self_study.py

The report identifies the resolved user-facing entrypoint as:
runtime.improvement_core_hf2_default.run_improvement_core_with_hf2

Controller:
IC-028

Regime:
091

Regime status:
COMPLETE

Terminal:
true

Mode:
EXPAND_OBSERVE_DECOUPLED

Execution truth:
IMPLEMENTATION_EXECUTED.

## Configured formal tools

The executed configured tools were:
- CurrentnessAudit
- RootCause
- QuestionWorthAsking
- ASSERT

Verification reports:
- configured_tool_execution_evidence = true
- all_configured_tools_full_36 = true
- core_files_present = true
- structured_handoff_loaded = true
- selected_candidate_reflects_handoff = true

Each serialized configured-tool recurrence used HF002 and reached RELATIVE_CLOSE.

## ImprovementCore selection

Selected candidate:
IC-HOST-CAPABILITY-DISCOVERY

Reason:
ordered upstream residual evidence supplied the uniquely strongest typed signal.

Current state:
ABSENT_IN_CORE_RUNTIME

Implementation status:
OPEN_HOST_BOUNDARY

Minimal candidate form:
typed adapter registry/discovery contract without self-authorizing use.

Architecture decision:
the upstream evidence changes priority toward typed host-capability/adapter discovery, while universal host authority remains external and the candidate is not self-admitted.

Admission result:
admitted_for_next_implementation_experiment = []

No implementation candidate was admitted.

## Other current candidates

Admission-ready:
IC-TRACE-EXPORT

Open design:
- IC-DURABLE-RUN-JOURNAL
- IC-HOST-CAPABILITY-DISCOVERY
- IC-RUNTIME-LIFECYCLE-FAILURE-SEMANTICS

Experiment-ready:
- IC-CAPABILITY-SKILL-PROMOTION
- IC-INTERFACE-QUALITY-BENCHMARK

Compose existing first:
IC-REFLECTION-EVIDENCE-SCHEMA

These remain candidates; the current run did not authorize mutation for them.

## HF2 disposition

Direct execution fact:
the selected user-facing entrypoint is run_improvement_core_with_hf2, so the complete ImprovementCore capability was run under the current HF002 local recurrence implementation.

The current self-study JSON report does not serialize the outer ImprovementCore hf2_status field. It does serialize the final COMPLETE terminal state and all configured-tool HF002 receipts.

Runtime reconstruction from runtime/improvement_core_hf2_default.py plus the reported successor:

1. the first complete ImprovementCore pass produces a material semantic state and therefore licenses local same-capability reapplication;
2. the successor preserves the same selected OPEN_HOST_BOUNDARY candidate and admits no implementation candidate;
3. unchanged operational receipts are excluded from semantic-change detection;
4. unchanged material reporting without semantic change is certified no-gain;
5. COMPLETE + no material semantic delta satisfies local_close;
6. HF002 disposition is therefore RELATIVE_CLOSE.

Outer HF2 disposition:
RELATIVE_CLOSE
(reconstructed from current runtime contract and the serialized final state; not directly emitted as a top-level field by self-study report 104).

## Governing result

No repository-owned mutation is licensed by this run.

The selected highest-priority candidate is blocked at the external host boundary.
The admission-ready trace-export candidate was not selected and cannot be substituted merely because it is easier to implement.

Current disposition:
CLOSED_RELATIVE_WITH_OPEN_HOST_BOUNDARY.

Reentry triggers include:
- a real host capability registry or adapter-discovery surface becoming available;
- new evidence that changes candidate ordering;
- admission of a different strict-gain candidate by the controller;
- a defeating witness against current host-boundary classification.
