# Architecture Scan 013

Date 2026-09-24

## Current architecture

Semantic algebra T = <K,S,O,G,M,C,R,U>
Controller state Z = <FT,X,A,Cl,B,E,L,Q,P>
Control levels:
L3 select/reconcile/reselect
L2 bind/checkpoint
L1 execute/capture

Observed loop:
L3 Select -> L2 Bind -> L1 Execute -> L2 Checkpoint -> L3 Consume/Reselect.

## Scan findings

A1 Semantic and realization architecture are correctly distinct.
No ninth semantic role is forced by activation.

A2 Activation bridge is presently a library, not yet the governing execution path.
Risk: architecture exists without universal enforcement.

A3 Identity is fragmented across C01-C49, B01-B58, CAP001-CAP033, runtime programs, repository tools and evidence receipts.
Risk: false completion through namespace-local coverage.

A4 Evidence is fragmented across CI, campaign prose and runtime artifacts.
Risk: claims require archaeology rather than queryable state.

A5 Historical equivalence is the largest unresolved preservation relation.
Fixture pass proves local implementation behavior, not predecessor reconstruction.

A6 Zero-request is architecturally central, not an optional late feature.
It tests whether L3 can select work without a supplied substantive job while L2 preserves observation-only authority and L1 executes only the bound observation.

A7 Boundary validation is underrepresented relative to observed defect frequency.
The dominant empirical defect class has been composition/interface failure.

A8 The linear capability-family sequence is an implementation convenience, not the controller's normative routing law.

## Required architecture repair

Introduce a machine evidence spine:

IdentityLedger
  -> SelectionReceipt
  -> BindingReceipt
  -> ExecutionReceipt
  -> CheckpointReceipt
  -> ConsumptionReceipt
  -> ReconstructionWitness
  -> ValidationDisposition.

Every readiness claim must resolve through this spine.

Controller invariant:
No claimed ToolUse/CapabilityUse without a complete evidence path appropriate to the claim.

Historical invariant:
HistoricallyReconstructed(h) only with an explicit predecessor behavior witness, successor program witness, frozen job/context, matched result relation, and preservation disposition.

Completion invariant:
Readiness is computed from evidence ledger state, never prose status or file existence.

## Architecture disposition

KEEP T.
KEEP L1/L2/L3.
KEEP DOS as controller-level observation program.
REPAIR activation integration and evidence spine.
DO NOT promote/migrate.
