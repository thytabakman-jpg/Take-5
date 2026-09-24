# Whole System Sweep 023

Date 2026-09-24
Scope Take-5 nonproduction
Basis EWG-ARCH-001

## MT result

The prior reply found the next obligation but still left continuation to a future turn. Under the new endogenous-work architecture that is a material mismatch.

## Root cause

The endogenous-work model and Improvement Core existed separately. There was no top-level executable composition whose job was to regenerate work after each admitted state change.

Root cause: TOP-LEVEL LIFECYCLE OWNERSHIP GAP.

Repair: system_loop.py now owns Generate -> Select -> Improvement Core -> Execute -> Discharge -> Regenerate -> Closure.

## Whole-system observation sweep

C01-C06 KEEP. Identity, typing, freeze, and external-dependence semantics survive.

C07-C14 KEEP. Dependency, representation, sensitivity, attribution, and challenge semantics survive. Their outputs can generate new work.

C15-C22 KEEP/PATCH ROLE. Novelty, diagnosis, recursive discovery, rivals, successors, and improvement-frontier outputs become candidate work or candidate objects before integration.

C23-C31 KEEP. Transfer, repair, compression, and architecture improvement survive with architecture-first currentness.

C32 PATCH ALREADY COMPLETE. Routing is obligation -> adequate reachable package rather than named-tool preference.

C33-C36 KEEP. Strict gain, regression, incomparability, and architecture recomputation survive.

C37-C43 KEEP. Provenance, license, target effect, coverage, rescue, disposition, and handoff survive.

C44-C48 KEEP with C47 clarification. Tool-relative closure does not imply system closure while fresh system work remains.

C49 KEEP. Corpus navigation can generate work but does not decide closure.

Improvement Core PATCH COMPLETE. It is adaptive policy/controller inside system_loop.

MTA KEEP.
Architecture Analysis STRENGTHENED: architecture basis is checked before component currentness.
PD/PDAudit KEEP.
GDOS KEEP as observation mode with two-timescale recursion.
Discriminator KEEP.
Reconciler KEEP.
Delegated Executor KEEP.
HF001 KEEP as reentry component.
TRC KEEP.
RTC KEEP.
Bias Perturbation KEEP.
Currentness Audit STRENGTHENED by reflexive architecture-first guard.
Capability Foundry KEEP.
Emergent Admission KEEP.
Historical Reconstruction KEEP with scoped claims.
Zero Request KEEP as no-job discovery entry.
Multi-Object KEEP.
Diagnosis/Root Cause KEEP.

## New objects

Endogenous Work Generator: admitted as lifecycle composition.
ResearchState/history closure: admitted as state/evidence realization.
Reflexive Currentness: admitted as strengthening composition.
SystemLoop: admitted as runtime composition.

No new primitive semantic role is required.

## Reconciled architecture

T=<K,S,O,G,M,C,R,U> remains.

System=<Interface,WorkLifecycle,ICPolicy,ConfiguredCapabilities,ResearchState,EvidenceHistory,Closure>.

WorkLifecycle owns continuation.
Improvement Core is a subsystem of System.

## Executed repairs

system_loop.py added.
system-loop tests added.
CAPABILITY_CURRENTNESS_MATRIX updated to EWG-ARCH-001.
C47/system-closure distinction corrected.
New architecture objects treated as composites rather than primitive expansion.

Next gate is regression plus fresh-work recomputation under this same basis.
