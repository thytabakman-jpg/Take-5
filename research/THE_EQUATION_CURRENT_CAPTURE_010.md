# THE EQUATION — Current Captured Form

Date: 2026-09-25
Status: SUPERSEDED BY research/THE_EQUATION_CURRENT_CAPTURE_012.md
Controller context: ICC / Improvement Core
Purpose: freeze the strongest current equation so later attacks improve from this exact object rather than reconstructing it from memory.

## Entry condition

Before substantive work, bind the entry contract:

EC(u,Z_0)
=
<FT,Controller,Mode_0,Boundary,Authority,Receipt>.

Required law:

Bound(EC) precedes SubstantiveTransition.

If Mode_0 = OBSERVE_DECOUPLED, run the frozen observer/DOS pass before goal-directed optimization, then reconcile that observation into the session state.

## Core inquiry round

Let the current inquiry architecture be:

G_Q = generate/instantiate the live question frontier from the current category basis and applicable 36 projections.

E_Q = realize the inquiry through adaptive selection/order, probe strategy, binding, execution, and returned evidence.

C_Q = reconcile/interpret/admit the returned information while preserving interaction, order effects, OPEN, BLOCKED, CONFLICT, and INCOMPARABLE.

U_Q = update governing inquiry state, including evidence, question frontier, category basis, coverage/currentness, and continuation-relevant memory.

One substantive round:

R_t
=
(U_Q o C_Q o E_Q o G_Q)(Z_t).

State-indexed expanded form:

R_t
=
U_Q(
  Z_t,
  C_Q(
    E_Q(
      G_Q(Z_t),
      Z_t
    ),
    Z_t
  )
).

## Tool Run Closure interleave

Every round crosses Tool Run Closure before recursion:

C_t
=
TRC(
  R_t,
  Z_t
).

TRC must return a typed disposition such as:
MATERIAL_CONSEQUENCE_CLOSED
NO_MATERIAL_CONSEQUENCE_CERTIFIED
OPEN
BLOCKED.

No material round is allowed to feed directly into the next recursive state without TRC unless an independently established continuation-equivalent no-effect rule licenses that omission.

## Session HF-001 wrapper

Update the recursive session state only after TRC:

Z_(t+1)
=
HF001_Update(
  Z_t,
  C_t
).

HF-001 reenters when:

Delta_result != 0
or
Delta_search != 0

provided a live admitted continuation remains.

HF-001 preserves:
- generated/admitted/material/blocked frontiers;
- evidence;
- result/search-state deltas;
- failure/subsumption memory;
- reversible reopenability;
- OPEN/BLOCKED;
- relative closure only.

## Current compact equation

Run_Q
=
HF001_session^TRC
[
  U_Q o C_Q o E_Q o G_Q
](Z_0).

This means:

1. bind the entry contract;
2. if required, observe first under DOS;
3. generate the live questions;
4. execute the inquiry;
5. reconcile/admit the results;
6. update the state;
7. close every material consequence through TRC;
8. let session HF-001 update/reenter on result or search-state delta;
9. stop only at basis-relative terminal closure or typed OPEN/BLOCKED.

## Current interpretation

The 22 recovered items are the current question-category basis carried inside state, not 22 fixed top-level questions.

The 36 architecture supplies state-dependent projections/applicability, not 36 new category identities.

The question basis can expand when Discovery produces an admitted genuinely new question family.

The outer equation is a session-level recursive inquiry system, not Basic Math, not one-pass question answering, and not a generic mathematical fixed point.

## OPEN

- whether G_Q, E_Q, C_Q, U_Q compress further without protected loss;
- exact minimal entry-contract representation;
- exact placement of observer-first policy;
- global completeness/minimality of the current question-category basis;
- empirical necessity of every 36 projection by job class;
- runtime realization of this exact semantic form;
- whether HF001_session^TRC admits a still shorter equivalent notation without hiding load-bearing behavior.

## Frozen current equation

Run_Q
=
HF001_session^TRC
[
  U_Q o C_Q o E_Q o G_Q
](Z_0).
