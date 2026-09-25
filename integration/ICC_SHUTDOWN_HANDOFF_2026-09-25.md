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
