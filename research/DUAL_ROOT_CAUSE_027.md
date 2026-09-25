# Dual Root Cause 027

Date 2026-09-24
Scope migration go/no-go episode plus subsequent execution failure

## Failure A

Observed:
The final go/no-go attack returned NO-GO because Reaserch draft PR 128 was newer than READINESS_EVIDENCE_024 and contained ten candidate semantic tools.

### Root-cause chain

Immediate error:
newer candidate research was treated as a blocking currentness delta before establishing that it had been admitted as load-bearing architecture.

Broken inference:
Newer(candidate) -> LoadBearing -> BlockingOPEN.

That inference is invalid.

PR 128 explicitly classified the ten objects as candidate semantic tools, denied runtime promotion/global novelty, and said stronger ablation/holdout work remained.

Deeper error:
Currentness discovery and currentness admission were collapsed.

Correct law:
Newer(x) -> ReviewRequired(x).
ReviewRequired(x) does not imply ArchitectureDelta(x).
ArchitectureDelta(x) requires materiality + admission/authority + result-sensitive effect on the current basis.

Deeper generator:
CANDIDATE-TO-GOVERNING-PREMATURE-PROMOTION.

This violated the system's own protected rule that evidence/candidates do not self-authorize.

Second failure:
Even after identifying a narrow residual, the controller stopped at NO-GO instead of using the user's granted repair authority to disposition the candidates and rerun the gate.

Generator:
OBSERVATION-TO-ACTION HANDOFF FAILURE.

The user asked for observe -> diagnose -> repair -> retest -> go/no-go.
The episode performed observe -> diagnose -> some repairs -> discovered candidate residual -> stopped.

### Required repair

1 Treat PR128 as REVIEW_REQUIRED, not blocking by age alone.
2 Run admission/materiality/novelty/composition tests on the ten candidates.
3 Only admitted result-sensitive survivors can invalidate the readiness basis.
4 Bind/repair survivors where licensed.
5 Rerun holdout/interactions/currentness/regression.
6 Then compute go/no-go.
7 Do not stop merely because a repairable residual was found.

## Failure B

Observed:
User explicitly requested:
root cause -> NT -> root cause -> NT -> root cause -> NT -> root cause.

Assistant returned only:
"I’ll run that exact alternating chain..."

No tool or analysis execution occurred.

### Root-cause chain

Immediate error:
imperative execution request was converted into a conversational acknowledgement.

Deeper error:
the assistant treated a statement of intended execution as if it were an execution receipt.

Formal mismatch:
Requested(ActionSequence) AND Licensed(ActionSequence)
but
Response = Promise(ActionSequence)
rather than
Response = Execute(ActionSequence) + Evidence.

Deeper generator:
INTERFACE-LEVEL SEMANTIC SIMULATION OF ACTION.

This is the same failure family previously identified for tools:
Available != Invoked
Selected != Executed
Intent != Receipt.

The configured-run/activation discipline existed inside the repository architecture but was not applied to the assistant's own conversational action boundary.

### Required repair

For executable user imperatives:
ACK is not a terminal state.
Completion requires either:
EXECUTED + receipt/evidence,
OPEN with exact blocker,
or BLOCKED with exact blocker.

A future-tense sentence cannot satisfy an execution request.

## Shared root

Both failures share one higher-order generator:

CONTROL LAW NOT SELF-APPLIED AT THE CONVERSATION BOUNDARY.

Internally the architecture requires:
candidate != admitted;
selected != executed;
evidence != authority;
bounded stop != closure.

The assistant violated those same distinctions externally:
candidate research was promoted into a blocker;
execution intent was promoted into execution.

Therefore the repair is not two unrelated patches.
The conversation interface must obey the same admission, activation, and closure laws as the research runtime.
