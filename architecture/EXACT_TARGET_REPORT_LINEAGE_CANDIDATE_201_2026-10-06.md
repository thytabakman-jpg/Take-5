# Exact Target and Report Lineage Candidate 201

Date: 2026-10-06
Status: IMPLEMENTED CANDIDATE / VALIDATION PENDING
Parent: issue #10 / PR #201
Source evidence: Reaserch PR #332 at c6397e20d0e3d4865142be95ab0f18b87557f6f9

## Problem

Take-5 already proves several nearby coordinates:

- which configured tool identity is current;
- whether a full configured tool invocation really executed;
- what causal execution-claim level is warranted;
- whether consequences are closed;
- whether the governing ImprovementCore job may return.

A separate target/evidence coordinate remained useful:

Which exact repository object/version was the run about, and does a required durable report prove lineage to that same immutable target?

This matters when a human-facing selector such as current/latest/main moves after a run or when work is accidentally begun in a legacy repository.

## Non-duplication

This candidate does not replace:

- Execution Claim Integrity 117;
- Protected Transition Integrity;
- Full Configured Tool Invocation 121;
- Tool Run Closure;
- ImprovementCore Parent Return Closure 139;
- Currentness Audit.

It composes with them.

Execution Claim Integrity answers how far the causal run progressed.

Exact Target Identity answers what immutable object the result is evidence about.

Report Lineage answers whether the required durable report exists and binds to that same target.

## Exact target identity

Runtime:

`runtime/exact_target_identity.py`

Target identity carries:

- repository;
- stable object ID;
- selector role;
- immutable identity kind;
- frozen reference;
- authority status.

For Git commits, the evidentiary target requires the full 40-character commit SHA.

Bare selectors such as `current`, `latest`, `main`, `master`, `head`, or `tip` cannot serve as immutable evidence identity.

When an expected canonical repository is supplied, a legacy-repository target fails with a canonical-repository conflict.

## Report lineage

Runtime:

`runtime/report_lineage.py`

A passing report lineage requires:

- exact run identity;
- valid exact execution target;
- valid exact report target;
- equality of the execution/report evidence keys;
- a causal execution claim at EXECUTED or stronger;
- durable report locator;
- report content identity;
- persistence witness;
- read-back verification;
- owner-routing disposition;
- affected-state disposition.

A persisted file without execution evidence cannot establish report lineage.

A report about a different immutable target cannot establish report lineage.

## Parent-return integration

`runtime/improvement_core_return_gate.py` now has an opt-in
`report_lineage_receipt_required` context coordinate.

When that coordinate is true, COMPLETE requires at least one report-lineage receipt and every
provided report-lineage receipt must pass. OPEN/BLOCKED/CONFLICT remain legal typed boundaries.

This keeps report closure at the existing parent return boundary instead of creating a new
parallel completion controller.

## Authority routing consequence

The target gate can also receive an expected canonical repository.

For the current migration basis:

`expected_repository = thytabakman-jpg/Take-5`

A target in `thytabakman-jpg/Reaserch` therefore cannot silently pass as the canonical execution
target merely because that legacy repository contains a newer commit.

## Regression set

Candidate tests:

- `tests/test_exact_target_identity.py`
- `tests/test_report_lineage.py`
- extended `tests/test_improvement_core_return_gate.py`

Required validation before admission:

1. Take-5 Validation passes on the exact candidate head.
2. Capability Preservation passes on the exact candidate head.
3. Existing ECI, PTI, currentness, Tool Run Closure, and parent-return tests remain green.
4. wrong-repository, moving-selector, short-SHA, missing-execution, wrong-report-target, and missing-report cases fail closed.
5. a valid report-bearing COMPLETE path remains reachable.

## Current claim

STRICT_GAIN_CANDIDATE.

Canonical admission remains OPEN until Take-5 validation and review/admission complete.
