# HF1 Mathematics 084

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE / VALIDATION REQUIRED

## Identity

HF1 is the governed reentry episode over admitted packet state.

It is not Tool Run Closure.
It is not the inner activation bridge.
It composes those objects.

## State

Let X be the typed packet space.

Each packet contains the K_PD coordinates plus three explicit reentry signatures:

w(x) = world_state
d(x) = discovery_state
r(x) = result_sensitive_state.

K_PD projection:

p_t = K_PD(x_t)

Obligations:

O_t = Omega(p_t).

## Package selection

Let C_i be the obligation cover of package i and c_i its cost.

HF1 chooses an exact sufficient package:

P*_t in argmin_P (sum_(i in P) c_i, |P|, lexical(P))

subject to

union_(i in P) C_i superset O_t.

If no sufficient package exists, terminal disposition is BLOCKED.

## Mode

m_t = M(x_t,O_t,P*_t).

If M is unresolved, disposition is OPEN.

## Execution sub-transition

The historical activation loop is now explicitly an inner transition:

e_t = Exec(P*_t,m_t,x_t).

Execution must be executed and consumed before HF1 proceeds.

## Consequence closure

c_t = C_TR(e_t,x_t).

C_TR remains Tool Run Closure and owns consequence harvesting, realization,
verification, consumption and typed CLOSED/OPEN/BLOCKED closure.

HF1 does not duplicate that job.

## Update and delta

After CLOSED Tool Run Closure:

x_(t+1) = packet(c_t).

Typed delta is exact signature inequality:

Delta_W(t) iff w(x_t) != w(x_(t+1))
Delta_D(t) iff d(x_t) != d(x_(t+1))
Delta_R(t) iff r(x_t) != r(x_(t+1)).

No hidden heuristic is used at the HF1 interface.

## Reentry law

rho(Delta_W,Delta_D,Delta_R) =

REENTER_OBSERVE  when Delta_W or Delta_D
REVERIFY         when not Delta_W and not Delta_D and Delta_R
NO_REENTRY       otherwise.

## Terminal law

HF1 terminates RELATIVE_CLOSE iff:

1. current Tool Run Closure status is CLOSED;
2. K_PD(x_(t+1)) exposes no live obligations;
3. any required REVERIFY has succeeded.

HF1 returns BLOCKED when:
- no sufficient package exists; or
- Tool Run Closure is BLOCKED.

HF1 returns OPEN when:
- mode is unresolved;
- execution is not consumed;
- Tool Run Closure is OPEN;
- a required delta signature is missing;
- REVERIFY is required but unavailable/fails;
- live obligations remain under NO_REENTRY;
- the resource bound is reached.

Otherwise it continues from x_(t+1).

## Unified recurrence

HF1(x_t) =

K_PD
-> obligations
-> exact sufficient package
-> mode
-> activation/execution subcycle
-> Tool Run Closure
-> typed packet update
-> Delta_W/Delta_D/Delta_R
-> rho
-> relative close / OPEN / BLOCKED / reentry.

This resolves the earlier two-loop residual:

the old activation loop is the execution sub-transition inside the HF1 governed episode,
not a separate governing controller.

## Runtime

runtime/hf1_episode.py

Regression:
tests/test_hf1_episode.py

Historical compatibility functions remain in runtime/hf_controller.py.

## Scope of completeness

This specification closes HF1 relative to its typed packet interface.

Domain-specific construction of world_state, discovery_state and
result_sensitive_state occurs upstream. HF1 requires those signatures and fails OPEN
when they are absent rather than guessing them.

Global minimality of the entire Take-5 controller is not claimed.
