# Goal-Decoupled Observation Sweep — DOS-001

Date 2026-09-24
Status candidate reusable method
Mode observation-first
Migration authority none

## Name

Goal-Decoupled Observation Sweep
Short name DOS.

The name refers to decoupling observation from the active optimization/solution goal during the sweep. It does not erase the governing project goal from the system. The goal is restored during reconciliation.

## Operator

DOS(X, boundary, B) = Reconcile({ Observe_b(X | boundary, optimization_pressure=0) : b in B })

where
X is the frozen observation object,
boundary fixes what counts as inside/outside the observation,
B is the selected behavior/lens set,
Observe_b returns structural consequences without being required to solve, improve, defend, or advance the current plan,
Reconcile occurs only after independent returns are complete.

## Required protocol

1 MTA preflight identifies X, boundary and contamination risks.
2 Freeze X.
3 Freeze boundary.
4 Explicitly suppress optimization, repair, successor-selection and solution pressure.
5 Run selected behaviors independently.
6 Preserve NO_DELTA, OPEN, conflict and strange observations.
7 Do not feed earlier behavior conclusions into later behavior prompts during the sweep.
8 Reconcile only after observation returns are complete.
9 Restore governing goal and authority constraints.
10 Recompute the work frontier from reconciled consequences.
11 Record whether DOS changed result, selector, architecture or nothing.

## Anti-contamination invariants

During observation:
No successor selection.
No repair.
No promotion.
No migration.
No requirement to validate current architecture.
No requirement to find a problem.
No requirement to be useful.
No cross-lens convergence pressure.

Observation result != action authorization.

## Replication evidence

Replication 010 applied the same structure to:
A the entire Take-5/Improvement Core project.
B the current campaign plan.

Whole-project run surfaced cross-cutting identity/evidence, boundary-failure, historical-equivalence, durable-state and end-to-end residuals.

Plan-only run exposed a hidden selector:
Next = next registry family.

Reconciliation replaced that default with a nondominated selector over information gain, goal impact, architecture risk, historical coverage, cost and authority safety.

These are two successful in-project replications. They support continued testing, not universal validity.

## Relationship to 12-before/12-after

12-before/12-after is an intervention protocol around a live job.
DOS is an observation protocol deliberately decoupled from the live job's optimization pressure.

They compose as:

MTA -> DOS -> reconcile -> choose job -> 12-before -> execute -> 12-after -> reenter.

DOS is therefore upstream of intervention when the object or plan itself needs structural inspection.

## Current consequence

Improvement Core must not default to the next registry family after DOS has changed the frontier.
Current high-value frontier includes:
historical reconstruction equivalence,
unified machine identity/evidence ledger,
cross-family interaction/ablation,
early zero-request/holdout,
and continued registry implementation.

Next work must be selected after reconciliation rather than inherited from pre-sweep momentum.
