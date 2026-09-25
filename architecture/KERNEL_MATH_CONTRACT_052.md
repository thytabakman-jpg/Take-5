# Kernel Math Contract 052

Date 2026-09-25

Status REVIEW ONLY MATH FREEZE

Runtime effect NONE

This artifact separates the mathematical objects that are currently easy to conflate.

```
S = <K, W_beta, IC, J, T>
```

K is the protected substrate law set.

W_beta is the math-first orchestration wrapper.

IC is the adaptive Improvement Core controller.

J is Jane as continuity supervisor.

T is the typed capability basis.

The key anti-loss rule is

```
change(one factor) != silently_redefine(other factors)
```

## 1. Kernel

The proposed exact kernel representation is a conjunction of legality laws rather than a master tool sequence.

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

Each symbol is independently recoverable.

### I_entry

```
SubstantiveAction(u,z) => Bound(beta)
```

Current realization

`runtime/entry_contract.py`

### I_identity

```
Target'(beta) = Target(beta)
Job'(beta) = Job(beta)
```

during one episode.

Current realization

`runtime/entry_contract.py`

`runtime/math_first_wrapper.py`

### I_surface

Recovered from Take Two.

```
Distinct(a,b) does_not_imply SeparateOperatingSurface(a,b)
```

A new surface is admitted only when no behaviorally sufficient view or composition already preserves the required semantics and the new surface demonstrates strict gain.

This is the mathematical form of the Take Two flexibility that was easy to lose when it was only remembered as a design feel.

Historical source

`thytabakman-jpg/Take-2/KERNEL.yaml`

`thytabakman-jpg/Take-2/ARCHITECTURE.md`

### I_transition

Also recovered from Take Two.

```
ConsequentialChange(z,z')
  => exists tau
     Authorized(tau)
     AND Applied(tau)
     AND Verified(tau)
```

### I_authority

```
Authority(out) subseteq Authority(beta)
```

Evidence does not self-authorize.

Child authority cannot exceed its grant.

### I_observe

```
O_beta(z)
```

is nonmutating with respect to live z.

Current realization passes a deep copy to the observer.

### I_freeze

```
mbar = Freeze(m)
Fingerprint(m_after_IC) = Fingerprint(mbar)
```

A mismatch blocks the episode.

### I_execution

```
CompleteExecution
  => Selected
     AND Bound
     AND Dispatched
     AND Started
     AND Executed
     AND Captured
     AND Consumed
```

Specified is not executed.

### I_admission

Persistent state is updated only across the Tool Run Closure admission boundary.

### I_open

OPEN, BLOCKED, and supported INCOMPARABLE states remain typed non-success states.

### I_closure

```
RelativeClose
  => chi = CLOSED
     AND R_Q(z_next) equiv_Q R_Q(z_now)
     AND no live reentry trigger
```

### I_lineage

Admitted material state changes remain reconstructible by version and provenance.

### I_reentry

```
material or result-sensitive delta
  => REENTER or REVERIFY
```

### I_promotion

No local component converts its own success into production authority.

## 2. Current executable wrapper

This is already implemented.

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

One round is

```
o_n            = O_beta(z_n)
m_n            = Phi(o_n,beta)
mbar_n         = Freeze(m_n)
g_n            = G(mbar_n,beta)
a_n            = A(mbar_n,g_n,z_n,beta)
y_n            = IC(a_n,z_n;T)
(c_n,chi_n)    = C_TR(z_n,y_n)
z_(n+1)        = U(z_n,c_n,chi_n)
j_(n+1)        = Sync_J(j_n,Delta z_n) when S_J(Delta z_n)=1
```

Current realization

`runtime/math_first_wrapper.py`

`runtime/tool_run_closure.py`

`runtime/jane_relevance.py`

## 3. Current executable Improvement Core

```
IC = mu X . (K_PD -> O -> M -> P -> E -> R_delta -> X)
```

The current historical selector remains available

```
score_i = |O intersect C_i|

P_hist = {i | score_i = max_j score_j > 0}
```

The opt-in math-first selector is

```
P*(m)
  in argmin_P sum_(T_i in P) c_i(m)
```

subject to

```
union_(T_i in P) C_i(m)
  superset O_exec(m)
```

plus applicability, licensing, type, authority, provenance, and protected-behavior constraints.

Current realization

`runtime/improvement_core.py`

`runtime/hf_controller.py`

`runtime/kpd_projection.py`

`runtime/mode_selector.py`

`runtime/math_first_selector.py`

## 4. Take Two recovered equation

Take Two's loop was

```
OBSERVE
-> FREEZE/TYPE
-> PD DISCOVER/CHALLENGE
-> DIAGNOSE when needed
-> DECIDE
-> TRANSITION
-> VERIFY
-> OBSERVE
-> REENTER
```

The reusable part is not the filename structure. It is the invariant package

```
F_T2 =
  minimal primitives
  + distinctions_without_surface_explosion
  + typed transition mutation
  + views_before_registries
  + strict_gain_admission
  + behavior_not_file migration
  + verified small-step evolution
```

That package can now be preserved or reintroduced explicitly rather than reconstructed from memory.

## 5. Alignment candidate

This is math only. It is not implemented on this branch.

The entry state is

```
theta = <G_ext, T, M, C, S, F>
```

G_ext is the external intended goal.

T is the target or referent.

M is controller, mode, and autonomy.

C is protected constraints and process invariants.

S is relevant state and baseline.

F is the completion predicate.

Instead of pretending hidden intent is directly observable, define the evidence-consistent candidate set

```
C(u,z,j,beta)
  = {theta | Consistent(theta,u,z,j,beta)}
```

Then define result-sensitive ambiguity

```
Amb_H(C)
  = {d |
       exists theta_1,theta_2 in C
       theta_1[d] != theta_2[d]
       AND ResultSensitive(d)}
```

The gate is

```
Proceed without clarification
  iff Amb_H(C) = empty
```

When it is nonempty, only one live result-sensitive coordinate is resolved before substantive execution.

Corrections are stored structurally

```
correction = <context, theta_hat, theta_user>

Delta_theta
  = {d | theta_hat[d] != theta_user[d]}
```

The learning target is Delta_theta, not the user's surface wording.

Candidate placement

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

Lambda is not allowed to weaken K.

## 6. Change protocol

A future one-letter change is evaluated against the dependency map before code changes.

For any proposed replacement x -> x'

```
Deps(x)
  = {
      protected invariants,
      behavioral witnesses,
      implementation paths,
      tests,
      downstream equations
    }
```

The change is admissible only when every protected behavior in Deps(x) is either preserved by x' or intentionally removed by an explicit reviewed decision.

The math remains versioned even when implementation changes, so a lost behavior has a precise equation to restore.

## Open coordinates

1. Whether the Take Two transition law becomes an explicit current Take-5 kernel guard or remains reconstructed through current admission and update machinery.

2. Whether the Take Two surface-minimality law is already fully realized by current architecture admission or requires executable enforcement.

3. The exact Lambda implementation and persistence semantics.

4. The matched historical corpus for validating high-alignment versus low-alignment runs.
