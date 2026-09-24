# DOS-003 — Pairwise Level Boundaries and Activation Bridge

Date 2026-09-24
Mode nonproduction observation
Migration/promotion prohibited

## MTA preflight
Target the two interfaces exposed by DOS-002 rather than the levels themselves:
B32 = L3 controller/reselection <-> L2 binding/checkpoint
B21 = L2 binding/checkpoint <-> L1 execution episode.

Optimization/repair pressure remains suppressed until reconciliation.

# Sweep A — B32 L3/L2

Frozen object
The contract by which L3-selected work becomes an L2 TaskFrame/TransitionContract and by which L2 checkpoint evidence returns to L3.

Independent structural returns

Goal Spine: boundary must preserve selected intent without silently expanding it.
Architecture: this boundary is a compiler boundary from control decision to executable bounded contract.
MTA: selection, binding and dispatch are distinct operations.
PD: correctness requires semantic preservation across representation change.
Multi-Object: a valid L3 selection plus valid L2 schema can still compose invalidly.
Diagnosis: missing explicit binding witness explains silent loss of selected behaviors.
Artifact Reality: stored selection does not prove bound contract.
Orphan/Ghost: selected behavior can disappear during binding; extra behavior can appear during binding.
Representation Attack: L3 policy objects and L2 contracts need not share representation.
Result Sensitivity: changing authority/scope/target during binding is material even when nominal behavior ID stays same.
RTC: L2 cannot replace selected work with a preferred successor without returning control.
HF/Reentry: checkpoint must report binding/execution deltas, not only result.
Authority: child contract authority <= controller grant.
Execution Truth: dispatch receipt must identify exact bound program and contract.
Boundary Analysis: boundary requires bidirectional witnesses.
Holdout: unfamiliar selection should bind without special-case code.
Ablation: removing binding validation permits authority and referent drift.
Zero-Request: observation work selected without substantive goal must remain observation-only after binding.
DOS: boundary itself can be frozen and swept independently.
Consequence Closure: any binding delta changes downstream execution interpretation.

Reconciliation B32

Define BindingReceipt:
BR=<episode,selection_id,program_id,target_id,job,authority_in,authority_out,contract_hash,deltas,status>

Required invariants:
authority_out <= authority_in
target_out == target_in unless typed/reapproved referent transition
job_out semantically preserves selected job
selected program is either bound or explicitly BLOCKED/OPEN
no silent substitution

Bind is therefore a checked compilation step, not mere serialization.

# Sweep B — B21 L2/L1

Frozen object
The contract by which an L2 bound TransitionContract is dispatched into an L1 execution and actual execution evidence returns.

Independent structural returns

Goal Spine: L1 realizes bounded work, not controller intent in the abstract.
Architecture: this is the realizability boundary.
MTA: dispatch, start, execution, success and consumption are non-equivalent.
PD: executable means there exists a valid realization path under environment/authority constraints.
Multi-Object: program + contract + environment interaction determines realizability.
Diagnosis: prior GitHub runner failure occurred here/upstream of Start; import-path failure occurred after Start but before semantic tests.
Artifact Reality: executable source file is weaker than successful realization.
Orphan/Ghost: bound work can become ghost if never dispatched/started.
Representation Attack: runtime command may differ from semantic program representation; witness must link them.
Result Sensitivity: environment and dependency differences can change result.
RTC: execution cannot self-promote successful output.
HF/Reentry: failure class must return to L2/L3 with typed stage.
Authority: L1 receives only effect-scoped authority.
Execution Truth: stage ledger required.
Boundary Analysis: environment E is explicit input to realization.
Holdout: novel program/environment pairing tests generic adapter.
Ablation: remove environment/schedulability check and host failure is misclassified as tool failure.
Zero-Request: L1 cannot manufacture a substantive job when executing observation contract.
DOS: observing runtime without repair pressure distinguishes substrate from semantic failure.
Consequence Closure: execution stage determines what claims are licensed upstream.

Reconciliation B21

Define ExecutionReceipt:
ER=<episode,binding_id,environment,dispatch,start,executed,exit,result_ref,evidence_ref,failure_stage>

Stage order:
BOUND -> DISPATCHED -> STARTED -> EXECUTED -> RESULT_CAPTURED -> CONSUMED

Failure stages include:
BINDING
DISPATCH
SCHEDULING
START
DEPENDENCY
EXECUTION
RESULT_CAPTURE
VERIFICATION
CONSUMPTION

# Cross-boundary reconciliation

The missing activation bridge is not one edge. It is a witnessed protocol:

L3 Select
 -> BR: L2 Bind/Validate
 -> Dispatch
 -> ER: L1 Execute/Capture
 -> L2 Checkpoint
 -> L3 Consume/Reconcile/Reselect.

ActivationComplete(e,p) iff
Selected(e,p)
AND ValidBindingReceipt(e,p)
AND Dispatched(e,p)
AND Started(e,p)
AND Executed(e,p)
AND ValidExecutionReceipt(e,p)
AND Consumed(e,p).

Capability availability is deliberately absent from the sufficiency claim: availability is a precondition, not evidence of activation.

# Architecture consequence

Add an activation/evidence protocol across existing levels.
Do not add a ninth semantic A5 role yet.
Do not collapse BR and ER: one proves semantic/authority-preserving compilation; the other proves realization.

# Next highest-information build experiment

Implement a minimal activation trace object and tests spanning:
1 successful selected->bound->executed->consumed path
2 selected behavior lost during binding
3 authority expansion during binding
4 bound but unscheduled execution
5 started but dependency failure
6 executed but unconsumed result
7 zero-request observation accidentally converted to substantive action

Then DOS the resulting executable bridge before broader family implementation resumes.
