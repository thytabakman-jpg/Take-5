# Improvement Core Run on One-Equation Question Compression 004

Date: 2026-09-25
Controller: current semantic IC-028
Input: research/ICC_ONE_EQUATION_QUESTION_COMPRESSION_003.md
Status: EXECUTED SEMANTIC RUN / MATERIAL SUCCESSOR

## Frozen job

Find the smallest faithful one-equation form that asks the full recovered question basis,
including applicable 36 projections, without losing question interaction, recursive question
generation, OPEN/INCOMPARABLE, verification independence, or current Improvement Core reentry.

## DISCOVER

The static candidate was:

M* = min { M : Recon(M,X) and Verified(M) and forall i Resolved(Q_i,M) }.

Material defects:

D1 STATIC CLOSURE
Several recovered question families generate new questions or materially alter other answer spaces.
A single forall over the initial 22 can close before the induced question frontier is exhausted.

D2 VERIFY DOUBLE COUNT
Verify Math is Q18, while Verified(M) also appears outside Closed^22.
Either verification is one inquiry obligation in the frontier or an admission/control predicate;
the static equation represented it twice without typing the distinction.

D3 QUESTION/CONTROL CONFLATION
The 22 are epistemic question nuclei. Admission, reconciliation, state update and reentry are not
additional questions. They must remain outside the question basis.

D4 INCOMPARABILITY LOSS
A scalar-looking min can suggest one unique model. Current IC preserves nondominated/incomparable
survivors unless a unique minimum is licensed.

D5 INTERACTION LOSS
Question answers can be noncommuting or jointly generate irreducible information. Independent
Resolved(Q_i,M) predicates do not represent this.

D6 36 APPLICABILITY DYNAMICS
Applicable/result-sensitive scope-mode cells can change after an answer is admitted. The projection
set must be state-indexed and recomputed on reentry.

## PLAN

Use one recursive inquiry-state equation.

Let Q22={Q1,...,Q22} be the recovered basis.
Let A_i(S) subseteq L36 be the currently applicable/result-sensitive projections for Qi.
Let Ans_J(Q_i o pi_l,S) be the answer/evidence returned by that inquiry.
Let Reconcile_J preserve conflicts, interactions, provenance and OPEN.
Let Adm_J license returned information to affect governing state.
Let U_J update state.

## Successor equation

S* =
Fix_{~J} [
  S |->
  U_J(
    S,
    Adm_J(
      Reconcile_J(
        { Ans_J(Q_i o pi_l,S)
          : i in {1,...,22}, l in A_i(S) }
      )
    )
  )
].

Equivalently, with the active inquiry frontier

Q_active(S) =
{ Q_i o pi_l : i in [22], l in A_i(S) },

S* =
Fix_{~J} [
  S |->
  U_J(
    S,
    Adm_J(
      Reconcile_J(
        {Ans_J(q,S): q in Q_active(S)}
      )
    )
  )
].

## Why this is stronger

1. All 22 question families enter through one answer operator.
2. The 36 geometry is a state-indexed projection surface, not multiplication of tool identity.
3. Answers are reconciled jointly before update, preserving Multi-Object interaction/noncommutation.
4. Admission remains distinct from asking/answering.
5. State update can generate new questions.
6. Fixpoint/reentry continues until no material continuation-relevant delta survives relative to J.
7. OPEN/CONFLICT/INCOMPARABLE are preserved through Reconcile/Adm rather than coerced to false completion.
8. Basic Math/minimal reconstruction remains one question inside Q22; it no longer illegitimately owns the outer architecture.

## Important correction

The earlier M* minimization form is useful as the Basic Math answer form.
It is not the correct universal outer equation for all 22 because it privileges reconstruction/minimization
as the container for question families that include goal, authority, novelty, discovery, transfer, causation,
currentness and completion.

The universal outer object is recursive inquiry-state closure.

## Compression

Define:

Inquiry_J(S) =
Adm_J(
  Reconcile_J(
    {Ans_J(q,S): q in Q_active(S)}
  )
).

Then the minimal readable outer equation is:

S* = Fix_{~J}( S |-> U_J(S,Inquiry_J(S)) ).

Do not treat Inquiry_J as primitive mathematics; it is only notation for the expanded set above.

## Completion boundary

This run establishes a material semantic successor to the static equation relative to the current recovered basis.

Still OPEN:
- global completeness of the 22 question-family basis;
- empirical necessity of every 36 cell by job class;
- runtime realization of IC-028 itself;
- proof that no stronger compression of the 22 erotetic nuclei exists.

## Verdict

STATIC_MIN_RECONSTRUCTION_OUTER_FORM = REJECT AS UNIVERSAL OUTER EQUATION.
RECURSIVE_INQUIRY_STATE_FIXED_POINT = CURRENT STRONGEST CANDIDATE.

The static minimization equation remains valid as a Basic Math/internal reconstruction question where its
job and order are licensed.
