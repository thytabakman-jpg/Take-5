# ICC Shutdown Handoff — 2026-09-25

Status: READY_TO_RESUME
Purpose: durable end-of-chat state
Canonical repository: Take-5
User-facing name: ICC

## Start rule

Do not reconstruct ICC from chat history.

For the next chat, read in this order:

1. `integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md`
2. `architecture/KERNEL_MATH_CONTRACT_052.yaml`
3. `architecture/KERNEL_MATH_CONTRACT_052.md`
4. `architecture/MATH_FIRST_WRAPPER_CLOSURE_039.md`
5. `architecture/IC_JANE_WRAPPER_MATH_PLAN_037.md`
6. `architecture/ARCHITECTURE_DECISION_036_MATH_FIRST_TOOL_SELECTION.md`
7. `architecture/LEARNING_TOOL_ADMISSION_DECISION_040.md`
8. `MIGRATION_STATE.yaml`

## ICC identity

ICC is the user-facing name for the current integrated Take-5 stack.

ICC does not create a second controller identity.

ICC denotes:

- Jane as entry/facade and continuity supervisor;
- the validated math-first wrapper;
- Improvement Core / IC-028 as adaptive controller;
- exact math-first least-cost package selection as an available selector;
- Tool Run Closure as consequence/verification/admission boundary;
- HF material-delta reentry as a distinct operator;
- C01-C49 plus PD/MT/root-cause/audit/architecture capabilities;
- the 36-cell coverage and directed-handoff structures;
- D4 plus typed D6/D8 and learning lenses;
- persistent lineage, authority, OPEN/BLOCKED preservation, and reentry.

## Current system factorization

The current system is now explicitly factored as:

```
S = <K, W_beta, IC, J, T>
```

where:

- K = protected substrate/transition laws;
- W_beta = math-first orchestration wrapper;
- IC = adaptive Improvement Core controller;
- J = Jane continuity supervisor;
- T = typed capability/tool basis.

Protected anti-loss rule:

```
change(one factor) != silently_redefine(other factors)
```

## Protected kernel candidate

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

This is a conjunction of governing laws, not a mandatory tool sequence.

Exact definitions and implementation mappings live in:

- `architecture/KERNEL_MATH_CONTRACT_052.yaml`
- `architecture/KERNEL_MATH_CONTRACT_052.md`

## Current executable wrapper

```
beta       = B_J(u)
o_n        = O_beta(z_n)
m_n        = Phi(o_n, beta)
mbar_n     = Freeze(m_n)
g_n        = G(mbar_n, beta)
a_n        = A(mbar_n, g_n, z_n, beta)
y_n        = IC(a_n, z_n; T)
(c_n,chi_n)= C_TR(z_n, y_n)
z_(n+1)    = U(z_n, c_n, chi_n)
j_(n+1)    = Sync_J(j_n, Delta z_n) when S_J(Delta z_n)=1
```

Composition:

```
W_beta
  = Sync_J
    o U
    o C_TR
    o IC
    o A
    o G
    o Freeze
    o Phi
    o O_beta
```

Relative closure requires:

```
chi_n = CLOSED
AND R_Q(z_(n+1)) equiv_Q R_Q(z_n)
AND no live reentry trigger
```

OPEN and BLOCKED remain typed non-success states.

## Current executable Improvement Core

```
IC = mu X . (K_PD -> O -> M -> P -> E -> R_delta -> X)
```

Historical selector remains available for compatibility:

```
score_i = |O intersect C_i|
P_hist  = {i | score_i = max_j score_j > 0}
```

Math-first selector:

```
P*(m) in argmin_P sum_(T_i in P) c_i(m)
```

subject to:

```
union_(T_i in P) C_i(m) superset O_exec(m)
```

plus applicability, licensing, type, authority, provenance, and protected-behavior constraints.

## Jane role

Jane remains a continuity supervisor and facade, not a competing solver.

```
j_(t+1) = U_J(j_t, delta_t)
```

only when the admitted delta is material and Jane-supervisory-relevant.

## Take Two behavior recovered in this chat

The useful Take Two property was recovered from the actual `thytabakman-jpg/Take-2` repository.

Core surface-minimality law:

```
Distinct(a,b) does_not_imply SeparateOperatingSurface(a,b)
```

New surfaces require:

```
AdmitNewSurface(x)
  => NOT ExistsBehaviorallySufficientViewOrComposition(x)
     AND StrictGain(x)
```

Take Two's compact substrate used:

```
Object
Relation
Event
Transition
Observation
```

with these additional preserved behaviors:

- consequential change goes through typed authorized transitions;
- views/compositions come before new registries/surfaces;
- capabilities migrate by behavior rather than file identity;
- architecture evolves through small verified transitions;
- observation precedes causal claims;
- evidence does not self-authorize;
- OPEN and incomparability remain preserved.

These are now explicit mathematical lineage candidates rather than an informal memory of the "Take Two feel."

## Alignment problem captured in this chat

The recurring ICC/user alignment problem is modeled as entry-state reconstruction.

```
theta = <G_ext, T, M, C, S, F>
```

where:

- G_ext = external intended goal;
- T = target/referent;
- M = controller, mode, and autonomy;
- C = protected constraints/process invariants;
- S = relevant state/baseline;
- F = finish/completion predicate.

Because intent is not directly observable:

```
C(u,z,j,beta)
  = {theta | Consistent(theta,u,z,j,beta)}
```

Result-sensitive ambiguity:

```
Amb_H(C)
  = {d |
      exists theta_1,theta_2 in C:
      theta_1[d] != theta_2[d]
      AND ResultSensitive(d)}
```

Candidate gate:

```
Proceed without clarification iff Amb_H(C) = empty
```

When nonempty, resolve only the highest-impact live coordinate before substantive execution.

Correction learning:

```
Delta_theta
  = {d | theta_hat[d] != theta_user[d]}
```

The system learns the wrong coordinate, not merely the user's wording.

Candidate placement:

```
beta      = B_J(u)
theta_hat = Lambda(u,z,j,beta)

O_(beta,theta_hat)
-> Phi
-> Freeze
-> G
-> A
-> IC
-> C_TR
-> U
-> Sync_J
```

Lambda is NOT IMPLEMENTED.

Lambda may constrain interpretation but may not weaken K.

## Historical alignment pattern identified

High-alignment runs repeatedly had:

- correct goal reconstruction;
- correct controller/mode selection;
- observer-first behavior when contamination risk existed;
- math formalization before architecture/tool choice;
- preservation of existing state and constraints;
- enough controller autonomy to choose and execute;
- explicit closure/reentry conditions;
- actual execution kept distinct from semantic description.

Painful runs repeatedly involved one or more of:

- generic ChatGPT behavior instead of ICC;
- wrong mode;
- acting before observation;
- literal prompt execution while missing the governing goal;
- state or constraint loss;
- handing decisions back unnecessarily;
- tool invocation without preserved purpose;
- analysis described as execution;
- no fixed closure predicate;
- corrections failing to change the underlying entry-state model.

The first validation task is to test this pattern empirically rather than treat it as settled.

## Learning-tool state preserved

The typed learning lenses remain first-class IC candidates only when their typed inputs exist:

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

Current learning-tool cost basis remains:

```
c_i = 1
basis = UNCALIBRATED_UNIT_COST
```

Do not infer empirical efficiency from this prior.

## Protected decisions

- Do not rebuild IC merely to solve the alignment problem.
- Do not rebuild Jane merely to solve the alignment problem.
- Do not silently mutate frozen mathematics.
- Do not collapse Tool Run Closure and HF delta reentry.
- Do not move problem-solving lenses into Jane.
- Do not make a lens mandatory merely because it exists.
- Do not delete Take Two recovered behavior during simplification.
- Do not change a mathematical symbol without tracing its dependent invariants, witnesses, implementation paths, tests, and downstream equations.
- Do not calibrate tool costs without execution evidence.
- Do not retire the legacy wrapper without a separate explicit cleanup decision.

## Validated implementation already in main

Math-first wrapper:

- PR #4
- merge `a567245bc62e3746f4fe5eaeec769a7d65245b72`
- validation run `36154766223`
- SUCCESS

Typed learning-tool admission:

- PR #5
- merge `4a5aef9d328023044e2ee18bcb691b009f2125a2`
- validation run `36164389061`
- SUCCESS

Kernel/alignment math freeze:

- PR #7
- merge `f51922e442000fb3ed950750112bfe6864214073`
- documentation-only
- runtime effect NONE

## Exact next-chat frontier

Resume in this order:

1. Build a matched corpus of historical high-alignment and low-alignment ICC episodes.
2. Reconstruct theta=<G_ext,T,M,C,S,F> for each episode.
3. Test whether result-sensitive entry-state error predicts the painful runs.
4. Use counterexamples to add/remove dimensions before implementation.
5. Decide whether Take Two I_surface needs an explicit executable Take-5 guard or is already fully reconstructed.
6. Decide whether Take Two I_transition needs an explicit executable Take-5 guard or is already fully reconstructed.
7. Specify Lambda exactly, including evidence inputs, ambiguity handling, correction learning, persistence, and reentry.
8. Implement Lambda only after the mathematics survives the matched corpus.
9. Run regression, observer-first, authority, OPEN/BLOCKED, Take Two flexibility, and unfamiliar holdout tests.
10. Only then consider runtime promotion.
11. After alignment work, return to the pre-existing empirical frontier: collect real ICC execution receipts and calibrate tool costs from evidence.
12. Legacy-wrapper retirement remains a separate later cleanup decision.

## Explicit OPEN ledger

These items remain unresolved and are intentionally recorded:

- Lambda implementation.
- Lambda persistence/update semantics.
- Historical matched alignment corpus.
- Empirical validation of Amb_H / Delta_theta as the useful predictor.
- Exact criterion for a "materially result-sensitive" alignment coordinate.
- Take Two I_surface placement/disposition.
- Take Two I_transition placement/disposition.
- Empirical tool-cost calibration.
- Legacy-wrapper retirement.
- Existing migration OPEN items in `MIGRATION_STATE.yaml`, including:
  - empirical IC030 dominance;
  - expand-outward-isolate matched ablation;
  - unrestricted candidate-universe completeness;
  - kernel global minimality;
  - historical backfill beyond current migration packet.

No runtime alignment behavior was changed in the closing chat. The math was frozen first.

## Resume instruction

A future chat begins from this file and `architecture/KERNEL_MATH_CONTRACT_052.yaml`.

Do not infer missing architecture from old chats when the repository contains the current object.

Do not treat candidate alignment mathematics as implemented behavior.

Do not skip directly to code before validating the mathematical object.
