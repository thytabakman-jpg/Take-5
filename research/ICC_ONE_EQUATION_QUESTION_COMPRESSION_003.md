# ICC One-Equation Question Compression 003

Date: 2026-09-25
Controller: IC-028 / ICC
Status: CURRENT CANDIDATE / CORRECTION TO INDEXED-QUESTION FORM

## Live issue

The recent indexed form

Q_all = {(i,a): i in [22], a in A_i, R_i(a)}

enumerates 22 question families but does not reproduce the earlier five-tool compression.

The earlier five-tool move was different in type:
it treated the component inquiries as obligations inside one reconstruction/optimization problem.

Therefore the full 22-family analogue must also be one model-selection/reconstruction equation.

## Correct compression target

Let Q_22={Q_1,...,Q_22} be the recovered question-family basis.

Let Resolved_J(Q_i,M) mean:
candidate model M supplies an admitted answer/disposition for Q_i sufficient for the protected continuation under J.

Let Recon_J(M,X) mean:
M reconstructs the protected behavior/evidence of X.

Let Verified_J(M) mean:
the required verification/attack obligations for M are terminally satisfied or explicitly OPEN/BLOCKED where the governing claim permits that state.

Then:

M^*_{22}(X|J,B)
=
min_preorder {
  M in M_B(X)
  :
  Recon_J(M,X)
  and Verified_J(M)
  and forall i in {1,...,22}, Resolved_J(Q_i,M)
}

Equivalent closure shorthand:

Closed^22_{J,B}(M)
iff
forall i in {1,...,22}, Resolved_J(Q_i,M).

So:

M^*_{22}(X|J,B)
=
min_preorder {
  M in M_B(X)
  :
  Recon_J(M,X)
  and Verified_J(M)
  and Closed^22_{J,B}(M)
}.

## Interpretation

This asks one question:

What is the smallest verified reconstruction of X that resolves every material question-family obligation in the current basis?

The 22 are therefore not invoked as 22 separate top-level questions.
They are constraints/obligations on one candidate reconstruction.

## Relation to 36

For l in L_36, a question-family obligation may be projected:

Resolved_J(Q_i o pi_l, M).

Only result-sensitive/applicable projections enter Closed^22.
The 36 architecture changes the obligation surface, not the outer equation.

## ICC verdict

The indexed set-builder answer was the wrong abstraction level.
Use one minimization/reconstruction equation with the question families internalized into the closure predicate.

Global minimality of the 22 basis remains basis-relative.
