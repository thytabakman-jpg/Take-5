# Architecture Decision 036 — Math-First Tool Selection

Date: 2026-09-25
Status: CHOSEN
Decision authority: IC synthesis across the current session and prior ImproveCore/Take work
Scope: control architecture, tool selection, and relation of D4/D6/D8 and framework-specific tools

## Decision

The canonical control direction is **math first, tools second**.

The system will not treat the growing tool inventory as the control architecture.

The control spine is:

[
Q_0
	o
operatorname{Observe}_{wide}
	o
operatorname{Formalize}
	o
operatorname{FreezeMath}
	o
operatorname{Goal}
	o
operatorname{Architect}
	o
operatorname{SelectTools}
	o
operatorname{Execute}
	o
operatorname{TRC}
	o
operatorname{HF1/Reentry}.
]

The wide observation phase is allowed to use broad coverage. Execution is selected only after the mathematical object and its obligations are fixed.

## Why this choice

Across the project history, the strongest results recur when the system:

- observes broadly before acting;
- identifies the mathematical obstruction/object before choosing machinery;
- preserves exact object identity, currentness, authority, and OPEN state;
- compresses equivalent tools/representations instead of accumulating names;
- uses architecture after the object is known;
- reenters after material deltas rather than treating one pass as closure.

Repeated failures recur when the system:

- starts from a tool inventory;
- promotes a recent attractive representation to authority;
- uses one fixed sequence for every problem;
- adds labels without specifying their mathematics;
- hides selectors, objectives, or applicability conditions;
- confuses coverage surfaces with executable tools;
- closes globally after a local no-gain result.

## Role of D4, D6, and D8

D4 remains the existing big-question/core transform and is not redefined here.

[
D_4:mathcal X	omathcal X.
]

D6 and D8 are selectable wrappers, not new global controllers:

[
oxed{D_6=Gammacirc D_4circSigma}
]

[
oxed{D_8=PicircGammacirc D_4circOmegacircSigma}
]

with

- (Sigma): Sense
- (Omega): Orient
- (Gamma): Ground
- (Pi): Prune

They are used only when their added operators are result-sensitive for the current mathematical object.

## Role of the framework tools

Kolb, DIKW, Predictive Processing, Functional Stack, OODA, Bayesian Update, Active Inference, Actor-Critic, and Rate-Distortion are typed **lenses/packages**.

They are not peers in a mandatory master sequence.

Their formal definitions live in:

- `architecture/LEARNING_OPERATOR_TOOLKIT_035.md`
- `runtime/learning_operator_tools.py`

## Role of the 36-cell systems

The canonical 36-cell Scope × ModeFace lattice remains a coverage/routing/challenge surface.

The 36-cell SourceScope × TargetScope graph remains a handoff/transport surface.

Neither is a list of 36 tools.

They help determine **where/how to inspect**, not what mathematical answer is true.

## Formal tool-selection rule

Let the frozen mathematical representation for question (q) be (m_q).

Let the unresolved obligations induced by that representation be

[
mathcal O(m_q)={o_1,dots,o_n}.
]

For each tool (T_i), define a contract

[
T_i=
langle
operatorname{In}_i,
operatorname{Out}_i,
A_i,
C_i,
c_i
angle
]

where:

- (operatorname{In}_i) is the required input type;
- (operatorname{Out}_i) is the output type;
- (A_i(m_q)in{0,1}) is the applicability predicate;
- (C_i(m_q)subseteqmathcal O(m_q)) is the obligation set the tool can address;
- (c_i(m_q)ge0) is execution cost.

The admissible tool set is

[
mathcal T_q=
{T_i:A_i(m_q)=1}.
]

The execution package is chosen by

[
oxed{
P^*(m_q)
in
argmin_{Psubseteqmathcal T_q}
sum_{T_iin P}c_i(m_q)
}
]

subject to

[
oxed{
igcup_{T_iin P} C_i(m_q)
supseteq
mathcal O_{mathrm{exec}}(m_q)
}
]

and all type, authority, provenance, and protected-behavior constraints.

Thus the system selects the **least-cost applicable package that covers the live execution obligations**.

This is the operational form of “derive the machinery from the problem rather than choose the problem-solving method first.”

## Broad observation versus narrow execution

Wide observation and minimal execution are not contradictory.

Observation may traverse a broad coverage surface to discover hidden coordinates:

[
m_q
=
operatorname{FreezeMath}
ig(
operatorname{Observe}_{wide}(Q_0)
ig).
]

After the object is frozen, tool selection contracts to the smallest package that can change the live result.

[
P^*=P^*(m_q).
]

Material deltas trigger reobservation and reselection:

[
Delta m
eq0
Rightarrow
operatorname{Observe}
	o
operatorname{Formalize}
	o
operatorname{SelectTools}
	ext{ again}.
]

## Canonical invariant

[
oxed{	ext{MATH BEFORE GOAL; GOAL BEFORE ARCHITECTURE; ARCHITECTURE BEFORE TOOL EXECUTION.}}
]

Tool names, repository recency, or prior success never substitute for applicability to the frozen mathematical object.

## Immediate consequence

Do not add another peer-level tool merely because a useful framework has been found.

A new framework is admitted only after:

1. its mathematical object is specified;
2. its input/output types are specified;
3. its selectors/objectives are explicit;
4. its applicability predicate can be stated;
5. it adds result-sensitive capability not already covered at lower cost.

Otherwise it remains evidence/reference material rather than an executable tool.
