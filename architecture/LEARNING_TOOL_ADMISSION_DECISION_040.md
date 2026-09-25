# Learning Tool Admission Decision 040

Date: 2026-09-25
Status: IMPLEMENTED_VALIDATED
Decision owner: IC
Scope: post-wrapper next action

## Choice

The next move after wrapper closure is not cost calibration, wrapper retirement, or another controller redesign.

The chosen move is to add a single typed admission bridge that makes the already-formalized learning tools available to Improvement Core only when their required runtime inputs are actually present.

This preserves the math-first rule:

[
	ext{mathematical object}
ightarrow
	ext{typed obligation}
ightarrow
	ext{applicability}
ightarrow
	ext{least-cost package selection}
ightarrow
	ext{execution}.
]

It does not make every lens globally applicable.

## Contract

For learning tool (T_i), define

[
T_i=
langle
I_i,
O_i,
A_i,
C_i,
c_i
angle
]

where:

- (I_i) is the required typed runtime input;
- (O_i) is the output type;
- (A_i(x)in{0,1}) is applicability to packet (x);
- (C_i) is the obligation covered by the tool;
- (c_i) is execution cost.

Applicability is

[
A_i(x)=1
iff
R_isubseteq Keys(x_i)
land
orall fin F_i, Callable(x_i[f]),
]

where (R_i) is the required-field set, (F_isubseteq R_i) is the callable-field set, and (x_i) is the lens-specific runtime input packet.

Missing inputs imply

[
A_i(x)=0.
]

They do not imply guessed defaults or invented evidence.

## Selection

The existing math-first IC selector remains:

[
P^*(x)
in
argmin_{Psubseteqmathcal T_x}
sum_{T_iin P}c_i
]

subject to

[
igcup_{T_iin P}C_i
supseteq
mathcal O_{mathrm{exec}}(x),
]

with

[
mathcal T_x={T_i:A_i(x)=1}.
]

If no applicable package covers the live obligation, the state remains OPEN.

## Cost status

Current learning-tool costs are deliberately neutral:

[
c_i=1.
]

Basis:

[
	exttt{UNCALIBRATED_UNIT_COST}.
]

These are priors for selection mechanics, not empirical efficiency claims.

Empirical calibration remains a later independent task.

## Admitted tool identities

| ID | Obligation |
|---|---|
| L-D6 | SENSE_CORE_GROUND |
| L-D8 | SENSE_ORIENT_CORE_GROUND_PRUNE |
| L-KOLB | EXPERIENTIAL_LEARNING_CYCLE |
| L-DIKW | DATA_TO_ACTION_MODEL |
| L-PP | PREDICTION_ERROR_MODEL_REVISION |
| L-BAYES | PROBABILISTIC_BELIEF_UPDATE |
| L-ACTIVE-INFERENCE | FREE_ENERGY_POLICY_SELECTION |
| L-ACTOR-CRITIC | REWARD_DRIVEN_POLICY_VALUE_UPDATE |
| L-RATE-DISTORTION | FIDELITY_CONSTRAINED_COMPRESSION |
| L-OODA | FEEDBACK_DECISION_ACTION |
| L-FUNCTIONAL-STACK | COUPLED_LAYER_UPDATE |

D4 remains the protected existing core operator and is supplied to D6/D8 as a typed runtime input rather than redefined by this bridge.

## Execution rule

For applicable (T_i):

[
x' = T_i(x_i)
]

and the tool's covered obligation is removed from the live obligation set only after execution returns.

Results are written to a separate learning-results coordinate with provenance by tool ID.

For inapplicable (T_i), the obligation is not discharged.

## Architecture placement

The bridge belongs behind IC.

It does not modify:

- Jane;
- the math-first wrapper;
- Tool Run Closure;
- the controller lease;
- C01-C49 semantics.

The bridge is separate from the historical C-capability registry because the learning lenses have different typed applicability contracts and are not historical C-capabilities.

Every admitted learning lens also receives a configured-run identity requiring:

- recursion;
- closure;
- reentry;
- external challenge when making a stronger terminal claim.

## Validation target

The candidate is acceptable only when all of the following hold:

1. missing inputs make a lens inapplicable;
2. supplied typed inputs make only that lens applicable;
3. IC can select and execute the lens through the exact least-cost selector;
4. successful execution discharges only its declared obligation;
5. missing inputs preserve OPEN;
6. D6 composition order remains Sense -> D4 -> Ground;
7. caller cost overrides work without rewriting the bridge;
8. all tool IDs and obligation IDs are unique;
9. every learning tool has a complete configured-run identity;
10. the full Take-5 validation gate passes.

## Validation evidence

Implementation merged through PR #5.

Merge commit:

`4a5aef9d328023044e2ee18bcb691b009f2125a2`

Main validation:

- GitHub Actions run `36164389061`
- conclusion: SUCCESS
- full pytest suite passed
- canonical whole-system audit passed
- closed-loop fixture passed
- zero-request dump passed

The typed bridge is now part of the canonical Take-5 runtime.

## Deferred choices

Do not calibrate tool costs until enough real execution receipts exist.

Do not retire the legacy wrapper as part of this change.

Do not move learning tools into Jane.

Do not force probabilistic, control-theoretic, experiential, or information-theoretic lenses onto problems lacking their required mathematical object.
