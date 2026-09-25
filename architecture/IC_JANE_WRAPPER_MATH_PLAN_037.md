# IC + Jane + Math-First Wrapper Plan 037

Date: 2026-09-25
Status: IMPLEMENTED_VALIDATED
Runtime changes: IMPLEMENTED via runtime/math_first_wrapper.py, runtime/math_first_selector.py, runtime/jane_relevance.py, plus narrow backward-compatible IC/HF extension points
Protected decision: do not rebuild IC or Jane; preserve current behavior and interfaces unless a narrowly-scoped verified patch is required. This constraint was preserved in implementation.\n\nImplementation merge: a567245bc62e3746f4fe5eaeec769a7d65245b72\nValidation: GitHub Actions run 36154766223 SUCCESS

## 1. Current Improvement Core mathematics

Let packet/state be (x\in\mathcal X).

### KPD projection

Let

[
F=\{identity,type,scope,job,readings,result\_sensitive,selectors,authority,provenance,open\}.
]

Define

[
K_{PD}:\mathcal X\to\mathcal K
]

with obligations

[
\mathcal O(x)
=
\mathcal O_0(x)
\cup
\{RESOLVE(f): f\in F,\;x_f=\bot\}.
]

### Current package selection

For program (i), let (C_i\) be its declared coverage and

[
s_i(x)=|\mathcal O(x)\cap C_i|.
]

Current runtime selection is

[
P_{current}(x)
=
\{i:s_i(x)=\max_j s_j(x)>0\}.
]

This is not yet the chosen math-first least-cost covering rule.

### Mode

[
M(x)\in
\{
EXPAND\_OBSERVE,
CONTRACT\_OBSERVE,
CONTRACT\_ACT,
EXPAND\_ACT
\}
\times
\{DECOUPLED,COUPLED\}
\cup\{OPEN\}.
]

### Decision

[
D_{IC}(x)=
\begin{cases}
CLOSE\_RELATIVE,&\mathcal O(x)=\varnothing\\
BLOCKED\_OPEN,&P_{current}(x)=\varnothing\\
OPEN,&M(x)=OPEN\\
EXECUTE(P_{current}(x),M(x)),&\text{otherwise}.
\end{cases}
]

### Execution and reentry

Let

[
x'_n=E_{P_n,M_n}(x_n).
]

The current delta router is

[
R_\Delta(x_n,x'_n)=
\begin{cases}
NO\_REENTRY,&x'_n=x_n\\
REENTER\_KPD,&K_{PD}(x'_n)\ne K_{PD}(x_n)\\
REVERIFY,&\text{otherwise}.
\end{cases}
]

IC iterates under seen-signature and round-budget guards.

## 2. Current Jane mathematics

Jane is a supervisory transducer/facade, not a competing solver.

Let Jane supervisory state be

[
j_t=(v_t,\Delta_t,A_t,R_t)
]

where (v_t\) is canonical version, (\Delta_t\) material deltas, (A_t\) alerts, and (R_t\) receipts.

### Entry binding

[
\beta_t
=
B_J(u_t;target,job,basis,authority,boundary,mode)
]

subject to

[
Valid(\beta_t)=1.
]

This freezes target, controller identity, initial mode, boundary and authority and establishes the controller lease.

### Capability coverage

[
Cov_J(b,tags,L)
\to
\{SELECTED,NON\_APPLICABLE,UNBOUND,BLOCKED,OPEN\}^{Programs}.
]

Jane reports coverage disposition; she does not grant authority.

### Delegation planning

[
Del_J(W,k)\to(Assignments,Incomparable)
]

with bounded (k\).

### Question frontier

[
Frontier_J(kind,detail,relevance)
=
\begin{cases}
PROBE\_CANDIDATE,&relevance=UNKNOWN\\
WORK\_CANDIDATE,&\text{otherwise}.
\end{cases}
]

### Supervisory synchronization

For material flag (m_t\), supervisory-relevance flag (s_t\), and delta (\delta_t\),

[
j_{t+1}
=
\begin{cases}
U_J(j_t,\delta_t),&m_t\land s_t\\
j_t,&\text{otherwise}.
\end{cases}
]

Jane does not own primary episode action selection while another controller holds the lease.

## 3. Missing mathematics

### IC gap A — selection mismatch

The chosen architecture requires tool contracts

[
T_i=
\langle In_i,Out_i,A_i,C_i,c_i\rangle
]

and

[
\mathcal T_m=\{T_i:A_i(m)=1\}.
]

Required package selection is

[
P^*(m)
\in
\arg\min_{P\subseteq\mathcal T_m}
\sum_{T_i\in P} c_i(m)
]

subject to

[
\bigcup_{T_i\in P} C_i(m)
\supseteq
\mathcal O_{exec}(m)
]

plus type, authority, provenance and protected-behavior constraints.

Do not rebuild IC. Replace/augment only its package-selection adapter after matched tests against current behavior.

### IC gap B — frozen mathematical object

IC currently selects from packet obligations. It needs an explicit optional input

[
m_q\in\mathcal M_q
]

that is already frozen by the wrapper. IC must not invent a new governing mathematical object during execution without triggering reentry.

### IC gap C — TRC naming collision

Two different operators currently carry TRC-like roles.

1. Tool Run Closure: consequence harvest -> disposition -> realize -> verify -> consume -> CLOSED/OPEN/BLOCKED.
2. (R_\Delta\): material-delta routing to NO_REENTRY / REENTER_KPD / REVERIFY.

Preserve both but give them distinct mathematical identities.

## 4. Jane gaps

### Jane gap A — supervisory relevance

The boolean supervisory_relevant is externally supplied. Define a predicate

[
S_J(\delta;m_q,\beta)
\in\{0,1\}
]

that is true exactly when the admitted delta changes a Jane-owned continuity coordinate such as currentness, open frontier, provenance/receipt state, canonical-version relation, unresolved handoff, or question-frontier state.

### Jane gap B — wrapper synchronization

Every admitted material wrapper update must call Jane synchronization when (S_J=1\). Jane remains sidecar/supervisor and never becomes the execution controller.

### Jane gap C — candidate handoff

Jane need not gain a new optimization engine. She can hand all typed candidates/incomparables to IC. IC remains the selection owner.

## 5. Wrapper rebuild from mathematics

This is the preferred rebuild target.

Inputs:

- user request (u\);
- system state (z_0\);
- Jane state (j_0\);
- tool registry (\mathcal T\);
- authority/context carried by the Jane entry binding.

### Stage 0 — Jane binding

[
\beta=B_J(u,z_0)
]

with

[
Valid(\beta)=1.
]

Jane's external job identity is protected. This is distinct from the operational goal derived later.

### Stage 1 — nonmutating observation

[
o_n=O_{\beta}(z_n).
]

Observation produces evidence without modifying (z_n\).

### Stage 2 — mathematical formalization

[
m_n=\Phi(o_n,\beta)
]

where

[
\Phi:\mathcal O_Q\to\mathcal M_Q.
]

The formalization must preserve all answer-relevant distinctions exposed by the observation.

### Stage 3 — freeze mathematics

[
\bar m_n=Freeze(m_n)
]

and (\bar m_n\) is immutable during the execution episode. A discovered result-sensitive mathematical delta triggers a new episode/reentry rather than silent mutation.

### Stage 4 — derive operational goal

[
g_n=G(\bar m_n,\beta).
]

The operational goal is derived from the frozen mathematical object while remaining constrained by Jane's protected external job/target.

### Stage 5 — architecture/compiler

[
a_n=A(\bar m_n,g_n,z_n,\beta)
]

where (a_n\) contains the typed obligations, dependency/order constraints, scopes, modes, selectors, authority requirements, and success conditions needed by IC.

### Stage 6 — IC

[
y_n=IC(a_n,z_n;\mathcal T).
]

IC owns adaptive package/mode selection, delegation and execution.

### Stage 7 — Tool Run Closure

[
(z_n^c,\chi_n)
=
C_{TR}(z_n,y_n)
]

where

[
\chi_n\in\{CLOSED,OPEN,BLOCKED\}.
]

Tool Run Closure accounts for downstream consequences before admission.

### Stage 8 — admitted update

[
z_{n+1}=U(z_n,z_n^c,\chi_n).
]

No hidden mutation is admitted.

### Stage 9 — Jane synchronization

[
j_{n+1}
=
\begin{cases}
U_J(j_n,\Delta z_n),&S_J(\Delta z_n;\bar m_n,\beta)=1\\
j_n,&\text{otherwise}.
\end{cases}
]

### Stage 10 — reentry

Let (R_Q(z)\) extract the question-relevant result.

Continue when there is a result-sensitive delta, unresolved closure state that is legally resumable, or a changed frozen-math obligation.

Relative fixed-point closure requires

[
\chi_n=CLOSED
\]

and

[
R_Q(z_{n+1})\equiv_Q R_Q(z_n)
]

and no reentry trigger remains.

OPEN and BLOCKED terminate the current episode as typed non-closure states, not as false success.

### Full wrapper

Define

[
W_\beta
=
Sync_J
\circ
U
\circ
C_{TR}
\circ
IC
\circ
A
\circ
G
\circ
Freeze
\circ
\Phi
\circ
O_\beta.
]

Then

[
(z_{n+1},j_{n+1})
=
W_\beta(z_n,j_n)
]

under guarded recursion until relative fixed point, OPEN, BLOCKED, or budget exhaustion.

This wrapper is allowed to be rebuilt greenfield because IC and Jane remain protected suboperators.

## 6. Tool placement

### IC-selectable research/processing packages

- D4 core operator.
- D6 = Ground o D4 o Sense.
- D8 = Prune o Ground o D4 o Orient o Sense.
- Kolb experiential cycle.
- DIKW project formalization.
- Predictive Processing.
- Bayesian Update.
- Active Inference.
- Actor-Critic.
- Rate-Distortion.
- OODA.
- Functional Stack.
- existing C01-C49 / PD / MT / root-cause / architecture / audit capabilities after typed applicability contracts.

These belong behind IC selection, not in Jane.

### Jane supervisory capabilities

- entry contract and controller lease;
- currentness/provenance checks;
- question-frontier watch;
- capability-coverage visibility;
- delegation packaging;
- material-delta synchronization;
- map/receipt/anti-loss continuity alerts.

Jane may observe outputs of IC tools but does not become their solver.

### Wrapper-owned machinery

- nonmutating observer;
- mathematical formalizer;
- FreezeMath contract;
- external-job vs operational-goal separation;
- compiler into IC packet;
- Tool Run Closure boundary;
- admitted update;
- Jane sync hook;
- global/relevant fixed-point termination.

## 7. Finish sequence

1. Freeze current IC and Jane behavior with regression tests.
2. Define (S_J\) supervisory relevance.
3. Rename/formally separate Tool Run Closure (C_{TR}\) from delta router (R_\Delta\).
4. Add frozen-math and typed-tool-contract inputs to IC without changing its outer loop.
5. Replace current max-hit package selection only after matched tests with (P^*\).
6. Build the new wrapper in parallel with current inquiry_session.py.
7. Run matched historical cases and unfamiliar holdouts.
8. Promote the wrapper only after behavioral preservation plus strict gain; retain old wrapper as rollback until then.

## Decision

Rebuild the wrapper from the mathematics up.

Do not rebuild IC.

Do not rebuild Jane.

Patch IC/Jane only at narrow typed interfaces required to make the new wrapper mathematically complete.
