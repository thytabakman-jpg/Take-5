# Full System Campaign Math — Show Me the Math

Date: 2026-09-26
Canonical repository: thytabakman-jpg/Take-5
Campaign: full-system-show-math-campaign-20260926

## 1. SHOW_ME_THE_MATH

For package P, formal object X, environment E, protected job J and basis K:

LB(P,X)
=
mu S .
(
Roots(P,X)
union
Union_(s in S) Dependencies_P(s)
).

DefinitionClosed(P,X,E)
iff
for every s in LB(P,X),

Defined_P(s)
or
(
TypedPrimitive_P(s)
and
Available_E(Provider_P(s))
).

ObligationClosed(P,Kind(X))
iff
for every o in Req(Kind(X)),

Satisfied_P(o)
or
(
NotApplicable_P(o)
and
Witness_P(o)
).

ShowMathComplete_(J,K)(P,X;E)
iff
DefinitionClosed(P,X,E)
and
ObligationClosed(P,Kind(X))
and
RealizerAvailable(P,E)
and
PortableEquivalent_(J,K)(Instantiate(P,E),X).

SMTM_(J,K)(P,X,E)
=
GREEN
when ShowMathComplete_(J,K)(P,X;E),

SMTM_(J,K)(P,X,E)
=
RED(Residuals(P,X,E))
otherwise.

Compact display normal form:

Σ = 𝟙_{Δ ∩ Ω ∩ Φ ∩ Ξ}

where the declared constants denote:

Δ = definition-closed region.
Ω = obligation-closed region.
Φ = realizer-available region.
Ξ = portable-equivalent region.
Σ = SHOW_ME_THE_MATH characteristic map.

The compact surface is not the complete portable package.

## 2. MT configured geometry

Run(MT)
=
Wrapper[MT^(D36_C)].

D36_C
=
S_scope x F_mode-face.

|S_scope| = 6.
|F_mode-face| = 6.
|D36_C| = 36.

Question projections:

22 x 36 = 792.

Cognitive projections:

4 x 36 = 144,

with

{DIFFERENTIATE, RELATE, RECONSTRUCT, STRENGTHEN}.

Mandatory black-box resolution spine:

PD
-> PDAudit
-> MTA
-> MT
-> PDAudit
-> C47.

MT return state:

MT_status
in
{CLOSED_RELATIVE, OPEN}.

## 3. Tool Conductor

Let I index the registered material-tool repertoire.

For each i in I:

a_i : X x C -> D_i union {OPEN_i}.

j_i : Y_i -> coproduct_(k in I) ({k} x Y_k).

Lifted factor:

T~_i(x,c)
=
BLOCKED_i
when no effective program witness exists,

T~_i(x,c)
=
OPEN_i
when a_i(x,c) is unresolved,

T~_i(x,c)
=
j_i(T_i(a_i(x,c)))
when admitted configured execution returns.

Exhaustive product:

TC_I(x,c)
=
( T~_i(x,c) )_(i in I).

Coverage invariant:

for every i in I,
exactly one conductor-level disposition is emitted.

Current registered cardinality:

|I| = 91.

Current compilation-witness partition:

60 self-contained factors,
31 portability-open factors.

Therefore:

Portable(TC_I) = false

under the current basis,

while exhaustive conductor disposition remains executable.

## 4. ICC128 Legacy frozen controller

ICC_128
=
C_128(Z_t,F_128,MI_t).

F_128
=
{L,O,R_123,D_PD,G,A,M_MT,T_2,E,V}.

MI_t
=
{I_t^k : k in Objects_t}.

I_t^k
=
<ObjectID,VersionID,Math,ComponentStatus,WholeStatus,Renderer,Freshness>.

Q_t
=
rho_128(Z_t,MI_t)
subseteq
F_128.

Y_t
=
Run_128(Q_t,Z_t,MI_t).

MI_(t+1)
=
Sync_128(MI_t,Y_t).

Z_(t+1)
=
U_128(Z_t,Y_t,MI_(t+1)).

Endogenous loop:

Z
-> G_Q
-> Q
-> G_W
-> W
-> S
-> W*
-> E
-> R
-> A
-> Z'
-> G_Q.

Terminal class:

tau_128
in
{COMPLETE,OPEN,BLOCKED,CONFLICT}.

Take-5 Legacy closure adds the reporting boundary:

LegacyRunClosed(r)
iff
GitHubReportCommitReceipt(r)
exists.

## 5. ICC130

No canonical Take-5 or Reaserch object is recovered for ICC130.

Therefore the only admissible current equation is:

ICC130
=
BLOCKED(IDENTITY_UNRECOVERED).

No ICC128/ICC123/ICC wrapper is substituted for ICC130.

## 6. Campaign GOAL

Let C be this campaign.

Goal(C)
=
Durable(
MT_request
and
MT_whole_conversation
and
GOAL_whole_conversation
and
ToolConductor_all_registered
and
TypedDisposition(ICC130)
and
ICC128Legacy_run
and
LegacyLearningReport
and
GiantReport
and
MathMarkdown
).

Campaign success condition:

Success(C)
iff
MT_request_dispositioned
and
MT_whole_conversation_dispositioned
and
GOAL_closed_relative
and
ToolConductor_coverage_complete
and
ICC130_typed_block_preserved
and
ICC128Legacy_controller_run_dispositioned
and
ICC128Legacy_report_receipt_exists
and
GiantReport_persisted
and
MathMarkdown_persisted.

## 7. Portability boundary

FreshCompatible(E)
does not mean
ZeroSemantics(E).

For SHOW_ME_THE_MATH:

PortablePackage + FreshCompatible(E)
=> protected behavior reconstructible.

RawEquation + ZeroSemantics(E)
does not imply execution.

For the current SHOW_ME_THE_MATH standalone realization:

CPython 3.12+ standard-library semantics
are an explicit environment primitive.

For ICC128 Legacy portable core:

typed host semantic/execution/controller bindings
are explicit environment primitives.

Exact Take-5 Legacy activation additionally requires:

TAKE5_GITHUB_REPORT_SINK.
