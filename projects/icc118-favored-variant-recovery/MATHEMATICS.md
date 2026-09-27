# Mathematics — Favored ICC118 Behavioral Successor Candidate

Status: CANDIDATE / NOT HISTORICAL IDENTITY CLAIM
Date: 2026-09-27

## 1. State

Let

```math
Z_t=
\langle
G_t,
S_t,
R_t,
E_t,
V_t,
Q_t,
W_t,
M_t,
B_t
\rangle
```

where:

- G_t = scoped parent goal;
- S_t = current substantive/project state;
- R_t = residual ledger;
- E_t = evidence/provenance;
- V_t = execution-reality state;
- Q_t = live question/discriminator frontier;
- W_t = candidate work frontier;
- M_t = negative/no-gain/route memory;
- B_t = authority, OPEN, BLOCKED and conflict state.

## 2. Reality separation

```math
V_t
=
SemanticAvailability_t
\times
RuntimeAvailability_t
\times
Authority_t.
```

Therefore:

```math
SemanticAvailable
\not\Rightarrow
RuntimeAvailable,
```

```math
RuntimeAvailable
\not\Rightarrow
Authorized,
```

and a runtime block does not erase semantic capability.

## 3. State-relative work generation

```math
Q_t
=
Gen_Q(G_t,S_t,R_t,E_t,M_t,B_t).
```

```math
W_t
=
Gen_W(Q_t,Z_t).
```

The next work is generated from the current state after admitted results, not from a frozen
historical battery.

## 4. Nondominated route selection

For preserving candidate work w define the routing vector:

```math
\nu_t(w)
=
\langle
Gain_t(w),
Leverage_t(w),
Continuation_t(w),
-Cost_t(w)
\rangle.
```

Then:

```math
Frontier_t
=
ND_{\succeq}
\{w\in W_t:Preserve_t(w)=1\}.
```

A cheap direct route is selected only when it dominates broader alternatives. Incomparable routes
remain plural.

## 5. Stewardship invariant

Let Owner(x) be the unique current authority for mutable project object x.

```math
StewardClosed_t
\iff
\forall x\in Required_t,|Owner(x)|=1
\land
HistoryPreserved(x)
\land
Evidence\neq Authority
\land
Semantic\neq Runtime.
```

A result in one dimension does not silently overwrite another dimension.

## 6. Completion enforcement

For residual r:

```math
Live(r,Z_t)
\iff
\neg Resolved(r)
\land
\left(
Work(r,Z_t)\neq\varnothing
\lor
\neg TerminalBoundary(r,Z_t)
\right).
```

```math
TerminalBoundary(r,Z_t)
\iff
BoundaryClass(r)\in
\{
ExternalControl,
UserAuthority,
EvidenceExhausted,
HistoricalEvidenceExhausted,
ConflictTerminal
\}
```

and

```math
CoverageAdequate(r)=1
\land
Work(r,Z_t)=\varnothing
\land
Reopen(r)\neq\varnothing.
```

Overall completion:

```math
Complete_{118^+}(Z_t)
\iff
ParentGoalSatisfied(G_t,S_t)
\land
\neg\exists r\,Live(r,Z_t).
```

## 7. Transition

```math
Z_{t+1}
=
U_{118^+}
\left(
Z_t,
Admit(
Execute(
Select(Frontier_t)
)
)
\right).
```

After a material admitted delta, regenerate Q, W and the frontier.

Unchanged failed/no-gain routes remain in M_t and do not count as progress.

## 8. Composite profile

The candidate is a profile, not a new primitive operator:

```math
ICC118^+
=
CompletionEnforcer
\circ
StewardshipGate
\circ
StateRelativeSelector
\circ
RealityGate.
```

Operational owners remain separate:

```text
ProjectManager -> project truth / authority / evidence / change / verification
ImprovementCore -> substantive autonomous solving
ICC128/current -> endogenous question/work reselection where selected
IC118 -> completion release gate
HF2 -> same-capability recurrence
```

## 9. Historical nonclaim

This mathematics is a 2026-09-27 successor reconstruction of the behavior the user repeatedly
sought under the "118" label.

It is not evidence that one historical ICC118 formal object already had this exact equation.
