# CURRENT EXECUTION CLAIM INTEGRITY — Recovery Anchor 117

Date: 2026-09-26
Status: CURRENT CANDIDATE / VALIDATED ON PR #113
Canonical repository: thytabakman-jpg/Take-5

## Purpose

Protect execution claims made by repository artifacts that sit outside the configured-tool
Protected Transition Integrity path.

This is not a replacement for PTI.

Configured tools remain governed by PTI.

## Core law

Execution claim levels:

IDENTIFIED
<
PLANNED
<
DISPATCHED
<
EXECUTED
<
CONSUMED
<
PERSISTED
<
VERIFIED.

For claim receipt r at level l:

ECI(r,l)=VERIFIED

iff every causal coordinate required up to l has non-empty evidence.

Otherwise:

ECI(r,l)=OPEN(Missing(r,l)).

## Current runtime

runtime/execution_claim_integrity.py

## Legacy integration

runtime/icc128_legacy_reporting.py

A bare GitHub learning-report receipt now proves persistence only.

Legacy closure requires an AttestedLearningReportReceipt whose execution claim reaches VERIFIED.

The causal route is:

controller invocation
-> run_result
-> report consumption
-> GitHub persistence
-> report verification.

Portable exact Legacy activation additionally requires:

TAKE5_GITHUB_REPORT_SINK

and

TAKE5_EXECUTION_CLAIM_ATTESTOR.

## Origin

Full MT:
artifacts/improvecore/MT_WHOLE_SYSTEM_HF2_CAMPAIGN_004_2026-09-26.md

Observer ImprovementCore + HF2:
artifacts/improvecore/IMPROVEMENTCORE_HF2_OBSERVER_CAMPAIGN_115_2026-09-26.md

Think-big selection:
artifacts/improvecore/IMPROVEMENTCORE_HF2_THINK_BIG_SELECTION_116_2026-09-26.md

Implementation:
architecture/EXECUTION_CLAIM_INTEGRITY_117.md

Closure receipt:
artifacts/improvecore/IMPROVEMENTCORE_HF2_THINK_BIG_FIX_CLOSURE_117_2026-09-26.md

## Validation

Take-5 Validation:
36267291930 SUCCESS.

Capability Preservation:
36267291918 SUCCESS.

## Boundaries

Repository-owned non-configured execution-claim seam:
CLOSED_RELATIVE after merge.

Universal host interception:
EXTERNAL_NOT_OWNED.

Universal HF2 wrapper promotion:
OPEN.
