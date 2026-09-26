# ICC128 Legacy learning-report contract

Status: REQUIRED / FAIL-CLOSED / EXECUTION-ATTESTED

The frozen ICC128 Legacy controller remains immutable.

Its within-run state and memory may change while it reasons. Those changes do not
become the starting memory of a later activation.

Every Legacy run must create a GitHub learning report.

Destination:

`thytabakman-jpg/Take-5/artifacts/icc128-legacy-learning/<run_id>.json`

A report is required for:

1. runs with material learning;
2. runs with no material learning;
3. runs that terminate OPEN, BLOCKED, CONFLICT, or COMPLETE;
4. failed runs.

The report records the initial state and memory, generated questions, generated
work, selected work, observed results, admitted deltas, state transitions, final
ephemeral memory, terminal status, and failure information when present.

## Execution-claim integrity

A persisted report is evidence of persistence.

It is not by itself evidence that the claimed controller run executed.

For an ordinary Legacy closure claim, the reporting path must causally witness:

identity
-> plan
-> dispatch
-> execution
-> consumption into the report
-> GitHub persistence
-> report verification.

The generic gate is:

`runtime/execution_claim_integrity.py`

The Legacy causal reporting path is:

`runtime/icc128_legacy_reporting.run_and_build_attested_learning_report`

followed by:

`runtime/icc128_legacy_reporting.require_attested_github_receipt`.

The first function invokes the supplied controller runtime itself before constructing
the report. The second upgrades the same execution claim through persistence and
verification.

A bare `LearningReportReceipt` proves persistence only and no longer closes the run.

## Closure invariant

Let `A(r)` be the verified execution-claim receipt for run `r` and `G(r)` the
GitHub learning-report receipt.

`LegacyRunClosed(r)`

iff

`A(r).level = VERIFIED`

and

`G(r)` exists.

Operationally:

`closure_allowed(receipt)`

returns true only for an `AttestedLearningReportReceipt` carrying both coordinates.

## Portable activation

The standalone portable Legacy activation now requires two explicit host primitives:

1. `TAKE5_GITHUB_REPORT_SINK`;
2. `TAKE5_EXECUTION_CLAIM_ATTESTOR`.

Therefore a report sink without execution attestation remains OPEN.

## Memory disposition

The report is the durable learning record. The controller's final learned memory is
discarded after the report is submitted.

The report does not authorize changes to the frozen snapshot, Reaserch, current ICC128,
or current ImprovementCore. Any later system may inspect these reports as evidence, but
evidence does not self-promote into current-system learning.
