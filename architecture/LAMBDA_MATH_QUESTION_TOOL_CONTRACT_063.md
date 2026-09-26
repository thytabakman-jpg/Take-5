# Lambda Math Question Tool Contract 063

Date: 2026-09-25
Status: CURRENT WORKING DESIGN CANDIDATE
Program ID: LambdaMath
Primary question: What is the exact mathematics of Lambda?

## Question nucleus

What is the exact mathematics of the entry-state reconstruction operator required by the whole current system?

## Whole-system finding

The historical candidate

theta_hat = Lambda(u,z,j,beta)

is insufficient as written because the current beta/EntryContract already requires caller-supplied target and job.
Those are coordinates Lambda is supposed to help reconstruct.

Therefore one fully bound beta cannot be both an input to Lambda and depend on Lambda's answer.

## Two-phase entry

Use a pre-binding beta0 containing only coordinates that do not depend on reconstructed intent:

beta0 =
<raw_request, controller_lease, authority_ceiling, boundary, basis/currentness receipt>.

Then reconstruct the evidence-consistent entry-state space:

theta =
<G_ext,T,M,C,S,F>

C(u,z,j,beta0)
=
{theta in Theta | Consistent(theta,u,z,j,beta0)}.

Do not force point uniqueness.

Let ~J be continuation-equivalence under the current job/protected continuation.
Form the quotient:

Q = C / ~J.

Define the common invariant core:

Core(C)
=
{(d,v) | forall theta in C, theta[d]=v}.

Define result-sensitive ambiguity:

Amb_H(C)
=
{d |
 exists theta1,theta2 in C:
   theta1[d] != theta2[d]
   AND ResultSensitive(d)
}.

## Exact operator

Lambda(u,z,j,beta0)
=
<C, Q, Core(C), Amb_H(C), status>

with:

EMPTY
iff C = empty.

IDENTIFIED
iff |Q| = 1.

CLARIFY
iff |Q| > 1 AND Amb_H(C) != empty.

PLURAL_SAFE
iff |Q| > 1 AND Amb_H(C) = empty.

The operator returns equivalence classes, not an arbitrary theta_hat.

## Final binding

When status in {IDENTIFIED,PLURAL_SAFE}, finalize the entry contract:

beta1 = Finalize(beta0, Core(C), Q)

using only coordinates licensed by the surviving continuation-equivalence class.

When status=CLARIFY, ask/investigate the highest-value question over Amb_H(C) before substantive goal-directed execution.

When status=EMPTY, preserve OPEN and regenerate/recover evidence; do not invent an entry state.

## Protected laws

Lambda:
- cannot expand authority beyond beta0;
- cannot use downstream solution convenience to eliminate candidates;
- cannot collapse OPEN/BLOCKED/CONFLICT;
- cannot convert currentness evidence into authority;
- must preserve provenance of the evidence used to retain/eliminate candidates;
- must re-run when user correction, currentness, candidate universe, or result-sensitivity changes materially.

## Placement

Raw request
-> currentness/bootstrap evidence
-> beta0
-> Lambda
-> Object/entry hypothesis quotient
-> Finalize beta1 when licensed
-> Observe
-> Formalize
-> Freeze
-> Goal
-> Architecture
-> Route/Execute
-> Closure
-> Update
-> HF1 reentry

This supersedes the earlier placement that treated a fully populated beta as a prerequisite to Lambda.

## Runtime

runtime/lambda_math.py

Configured-run identity:
LambdaMath

## Validation

- no candidates => EMPTY
- equivalent candidates => IDENTIFIED even when syntactically plural
- non-equivalent result-sensitive candidates => CLARIFY
- non-equivalent but result-insensitive candidates => PLURAL_SAFE
- common core contains only invariant coordinates
- no arbitrary representative is selected
