# ICC Shutdown Handoff — 2026-09-25

Status: READY_TO_RESUME
Purpose: durable end-of-chat state
Canonical repository: Take-5
User-facing name: ICC

## ICC identity

ICC is the user-facing name for the current integrated system.

It is **not** a second controller and does not replace the identities already protected in the runtime.

ICC denotes the composition of:

1. Jane entry/facade and supervisory continuity layer.
2. The validated math-first wrapper.
3. Improvement Core / IC-028 as the adaptive controller.
4. The exact math-first least-cost tool selector.
5. Tool Run Closure as the consequence/verification/admission boundary.
6. HF material-delta reentry routing as a distinct operator.
7. The C01-C49 capability family and existing PD/MT/root-cause/audit/architecture machinery.
8. The 36-cell coverage and handoff structures.
9. D4 as the protected big-question/core operator.
10. D6, D8, and the admitted learning lenses through the typed learning-tool bridge.
11. Jane synchronization after admitted continuity-relevant material deltas.

No new authority layer is created by the label ICC.

## Canonical wrapper mathematics

Let

[
eta=B_J(u)
]

be Jane's bound entry contract.

For each round:

[
o_n=O_eta(z_n)
]

[
m_n=Phi(o_n,eta)
]

[
ar m_n=Freeze(m_n)
]

[
g_n=G(ar m_n,eta)
]

[
a_n=A(ar m_n,g_n,z_n,eta)
]

[
y_n=IC(a_n,z_n;mathcal T)
]

[
(c_n,chi_n)=C_{TR}(z_n,y_n)
]

[
z_{n+1}=U(z_n,c_n,chi_n)
]

and Jane synchronization is

[
j_{n+1}
=
egin{cases}
U_J(j_n,Delta z_n),
&S_J(Delta z_n;ar m_n,eta)=1\
j_n,
&	ext{otherwise}.
end{cases}
]

So

[
W_eta
=
Sync_J
circ U
circ C_{TR}
circ IC
circ A
circ G
circ Freeze
circPhi
circ O_eta.
]

Relative closure requires:

[
chi_n=CLOSED
]

[
R_Q(z_{n+1})equiv_QR_Q(z_n)
]

and no live reentry trigger.

OPEN and BLOCKED remain legitimate non-closure states.

## Canonical IC tool-selection mathematics

For frozen mathematical object (m), each tool has contract

[
T_i=
langle
I_i,O_i,A_i,C_i,c_i
angle.
]

The applicable set is

[
mathcal T_m={T_i:A_i(m)=1}.
]

IC selects

[
P^*(m)
in
argmin_{Psubseteqmathcal T_m}
sum_{T_iin P}c_i(m)
]

subject to

[
igcup_{T_iin P}C_i(m)
supseteq
mathcal O_{mathrm{exec}}(m)
]

plus type, authority, provenance, and protected-behavior constraints.

The historical max-hit selector is retained as compatibility/rollback behavior.

## Learning-tool admission

The following are now first-class IC candidates when their typed inputs exist:

- L-D6
- L-D8
- L-KOLB
- L-DIKW
- L-PP
- L-BAYES
- L-ACTIVE-INFERENCE
- L-ACTOR-CRITIC
- L-RATE-DISTORTION
- L-OODA
- L-FUNCTIONAL-STACK

Missing runtime inputs imply

[
A_i(x)=0.
]

No guessed data, likelihoods, utilities, distortion functions, grounding sources, or environment dynamics are manufactured merely to run a tool.

Current learning-tool costs are

[
c_i=1
]

with basis

`UNCALIBRATED_UNIT_COST`.

This is an explicit neutral prior, not an empirical efficiency claim.

## Protected decisions

Do not rebuild IC.

Do not rebuild Jane.

Do not silently mutate frozen mathematics.

Do not collapse Tool Run Closure and HF delta reentry routing back into one operator.

Do not move problem-solving lenses into Jane.

Do not make a lens globally mandatory merely because it exists.

Do not calibrate relative tool costs until real execution receipts provide evidence.

Do not retire the legacy wrapper without a separate explicit cleanup decision.

## Validated implementation

Math-first wrapper:

- PR #4
- merge `a567245bc62e3746f4fe5eaeec769a7d65245b72`
- main validation run `36154766223`
- SUCCESS

Typed learning-tool admission:

- PR #5
- merge `4a5aef9d328023044e2ee18bcb691b009f2125a2`
- main validation run `36164389061`
- SUCCESS

Both validation gates included the full pytest suite, canonical whole-system audit, closed-loop fixture, and zero-request dump.

## Current canonical files

Start with:

1. `README.md`
2. `integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md`
3. `architecture/LEARNING_TOOL_ADMISSION_DECISION_040.md`
4. `architecture/MATH_FIRST_WRAPPER_CLOSURE_039.md`
5. `architecture/OBSERVER_ALL_TOOLS_SWEEP_038.md`
6. `architecture/IC_JANE_WRAPPER_MATH_PLAN_037.md`
7. `architecture/ARCHITECTURE_DECISION_036_MATH_FIRST_TOOL_SELECTION.md`
8. `runtime/math_first_wrapper.py`
9. `runtime/math_first_selector.py`
10. `runtime/learning_tool_bridge.py`
11. `runtime/improvement_core.py`
12. `runtime/jane.py`

## Current frontier

There is no blocking IC/Jane/wrapper architecture problem left from this session.

The next highest-value frontier is empirical:

1. collect real ICC execution receipts;
2. measure runtime/coverage/gain/regression behavior by tool;
3. estimate evidence-based tool costs (c_i);
4. test whether learned costs improve package selection;
5. only then replace the neutral unit-cost prior.

A separate later cleanup decision can evaluate legacy-wrapper retirement after sufficient live comparison evidence exists.

## Resume instruction

When returning to this project, treat this file and the current Take-5 README as the session source of truth.

Resume from the empirical cost-learning frontier unless a newer admitted material delta supersedes it.

Do not reconstruct this architecture from chat history.


## Alignment and kernel-math closure from the final chat

This chat added a new material result that supersedes the prior empirical-only resume frontier.

The user identified a recurring ICC/user alignment problem: some runs reconstruct the intended goal, controller mode, protected constraints, current state, and finish condition correctly and feel highly effective; other runs begin substantive work from the wrong entry state and require repeated correction.

The alignment problem is now represented mathematically rather than as a prose preference.

Let

```
theta = <G_ext, T, M, C, S, F>
```

where:

- G_ext = external intended goal;
- T = target/referent;
- M = controller, mode, and autonomy;
- C = protected constraints and process invariants;
- S = relevant state/baseline;
- F = completion predicate.

Because user intent is not directly observable, define the evidence-consistent candidate set

```
C(u,z,j,beta) = {theta | Consistent(theta,u,z,j,beta)}
```

and the result-sensitive ambiguity set

```
Amb_H(C)
  = {d |
      exists theta_1,theta_2 in C:
      theta_1[d] != theta_2[d]
      AND ResultSensitive(d)}
```

The candidate gate is

```
Proceed without clarification iff Amb_H(C) = empty
```

When nonempty, resolve only the highest-impact live coordinate before substantive execution.

User corrections are represented structurally:

```
Delta_theta
  = {d | theta_hat[d] != theta_user[d]}
```

The intended learning target is the coordinate error, not the wording of the correction.

This alignment operator is NOT IMPLEMENTED yet.

### Math-first anti-loss decision

Before changing alignment behavior, the current system was factored into explicit mathematical objects:

```
S = <K, W_beta, IC, J, T>
```

K = protected substrate laws.

W_beta = current math-first orchestration wrapper.

IC = adaptive Improvement Core controller.

J = Jane continuity supervisor.

T = typed capability/tool basis.

The protected kernel candidate is

```
K =
  I_entry
  AND I_identity
  AND I_surface
  AND I_transition
  AND I_authority
  AND I_observe
  AND I_freeze
  AND I_execution
  AND I_admission
  AND I_open
  AND I_closure
  AND I_lineage
  AND I_reentry
  AND I_promotion
```

This is a conjunction of transition-legality/preservation laws, not a tool sequence.

The key anti-loss rule is:

```
change(one factor) != silently_redefine(other factors)
```

A future symbol change must carry an explicit dependency set containing protected invariants, behavioral witnesses, implementation paths, tests, and downstream equations.

### Take Two behavior recovered explicitly

The property repeatedly remembered as the useful Take Two flexibility was recovered from the actual Take-2 repository.

Core laws:

```
Distinct(a,b) does_not_imply SeparateOperatingSurface(a,b)
```

and

```
AdmitNewSurface(x)
  => NOT ExistsBehaviorallySufficientViewOrComposition(x)
     AND StrictGain(x)
```

Take Two also used the five primitive substrate:

```
Object, Relation, Event, Transition, Observation
```

with consequential mutation routed through typed authorized transitions, views/compositions preferred over new registries, capability migration by behavior rather than file identity, and architecture evolution through small verified changes.

These behaviors are now represented in the math contract and no longer depend on remembering a Take Two "feel."

### Durable math artifacts

Canonical review artifacts added in this chat:

- `architecture/KERNEL_MATH_CONTRACT_052.yaml`
- `architecture/KERNEL_MATH_CONTRACT_052.md`

They map the mathematical terms to current implementation paths and explicitly separate current executable behavior from candidate alignment mathematics.

## Current resume frontier after this chat

The next chat begins from the math artifacts above. Do not reconstruct the model from chat history.

Priority order:

1. Validate the proposed kernel factorization against historical high-alignment and low-alignment ICC runs.
2. Build the first matched alignment corpus and test whether errors in <G_ext,T,M,C,S,F> explain the painful runs.
3. Decide whether the Take Two I_surface and I_transition laws require explicit executable Take-5 guards or are already fully realized by current admission/update machinery.
4. Specify Lambda, the alignment reconstruction operator, including persistence and correction-update semantics.
5. Only after 1-4, implement Lambda as an entry-stage extension that cannot weaken K.
6. Run matched regression, holdout, observer-first, authority, OPEN/BLOCKED, and Take Two flexibility tests before any promotion.
7. Continue the prior empirical frontier: collect real ICC execution receipts and calibrate tool costs only from evidence.
8. Legacy-wrapper retirement remains a separate later cleanup decision.

## Items intentionally left OPEN

These are not forgotten work:

- exact implementation of Lambda;
- exact persistence model for alignment corrections;
- selection of the historical matched alignment corpus;
- empirical test of Delta_H / Amb_H as a predictor of successful versus painful runs;
- disposition of Take Two I_surface as explicit executable guard versus already-reconstructed invariant;
- disposition of Take Two I_transition as explicit executable guard versus already-reconstructed invariant;
- empirical tool-cost calibration;
- legacy wrapper retirement;
- broader pre-existing migration validation items in MIGRATION_STATE.yaml.

No runtime alignment behavior was changed in this chat. That is deliberate. The math was frozen first.
