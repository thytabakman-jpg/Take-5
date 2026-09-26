# Most-Effective Objective Compilation 001

Date: 2026-09-26
Status: CANDIDATE RUNTIME REPAIR
Source: ImproveCore run over the current conversation

## Failure

The user explicitly selected "most effective" rather than "smallest" or "least cost".

The current math-first selector minimizes declared execution cost after obligations are fixed.

That selector is valid only after the effectiveness criterion has already been represented in the protected job/obligation state.

Otherwise:

MOST_EFFECTIVE
can be silently replaced by
MIN_EXECUTION_COST.

That is a load-bearing semantic/runtime substitution.

## Repair

Keep cost minimization downstream.

When:

selection_objective = MOST_EFFECTIVE

the protected effectiveness coordinates must first compile into K_PD obligations.

For this campaign the recovered coordinates are:

- RecoveryCoverage
- CanonicalIntegration
- ProtectedBehaviorPreservation
- ResidualDiscovery
- ExecutionReality
- ClosureQuality
- FutureReachability
- UserRepromptReduction

If no coordinates are supplied, the system emits:

RESOLVE_EFFECTIVENESS_OBJECTIVE

and remains OPEN rather than silently treating cost as the objective.

If coordinates are supplied, each becomes an obligation:

EFFECTIVENESS_<COORDINATE>.

The ordinary package selector may then minimize cost only among packages whose declared coverage satisfies the compiled live obligations.

## Consequence

This does not replace the math-first selector.

It restores the correct order:

GOAL/OBJECTIVE
-> PROTECTED EFFECTIVENESS COORDINATES
-> OBLIGATIONS
-> APPLICABILITY/COVERAGE
-> COST MINIMIZATION.

Thus "most effective" and "least cost among packages satisfying the effectiveness-derived obligations" are no longer conflated.

## Current authority

Runtime change is proposed through PR/validation.
No semantic completeness claim is made for the effectiveness coordinate set outside its declared campaign basis.
