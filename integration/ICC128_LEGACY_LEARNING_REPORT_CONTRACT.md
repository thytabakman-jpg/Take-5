# ICC128 Legacy learning-report contract

Status: REQUIRED / FAIL-CLOSED

The frozen ICC128 Legacy controller remains immutable.

Its within-run state and memory may change while it reasons. Those changes do not
become the starting memory of a later activation.

Every Legacy run must instead create a GitHub learning report.

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

Closure invariant:

`LegacyRunClosed(run) iff GitHubReportCommitReceipt(run) exists`

The report is the durable learning record. The controller's final learned memory
is discarded after the report is submitted.

The report does not authorize changes to the frozen snapshot, Reaserch, current
ICC128, or current ImprovementCore. Any later system may inspect these reports as
evidence, but evidence does not self-promote into current-system learning.
