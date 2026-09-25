# ICC Historical Repair Pattern + Big Equation Runtime Realization 013

Date: 2026-09-25
Controller: ICC / current semantic IC-028
Status: IMPLEMENTED + REGRESSION VALIDATED / NO RUNTIME PROMOTION

## Frozen target

Close the remaining runtime gap behind:

Run_Q(u,Z_0)
=
HF001_session^TRC
[
  U_Q o C_Q o E_Q o G_Q
]
(
  P_{PEC(u,Z_0)}(Z_0)
)

without creating another controller or replacing existing HF-001 machinery.

## Historical repair pattern recovered

Across prior successful repairs, the recurring pattern is:

1. freeze the real observed failure;
2. localize the earliest divergence;
3. reuse already-established semantics rather than inventing another conceptual layer;
4. build a thin executable facade at the missing transition;
5. fail closed on missing evidence/authority/binding;
6. emit execution/closure receipts;
7. regression-test the original failure trace;
8. update current-state surfaces only after the regression passes.

Relevant precedents:
- REAL_TASK_ENTRY_REGRESSION_2026-09-23.md
- IC-022_AUTONOMOUS_RUN_006_EXECUTABLE_TRANSITION_VALIDATOR_2026-09-24.md
- MTA_WRAPPER_AND_SELF_HF001_RECURSIVE_001_2026-09-24.md
- TOOL_RUN_CLOSURE_SELF_APPLICATION_001_2026-09-24.md
- TURN_ENTRY_TOOL_ORCHESTRATION.md
- existing Take-5 runtime/recursive_episode.py

## Repair chosen

Do not build another controller.

Reuse:
- entry_contract.py for PEC;
- Jane begin_turn for entry binding;
- existing recursive_episode.py as HF-style recursive host;
- canonical TRC semantics for closure behavior.

Add only the missing runtime pieces.

## Runtime implementation

### Generic Tool Run Closure

New:
runtime/tool_run_closure.py

It realizes the generic orchestration:

Harvest
-> exact typed consequence identity
-> disposition
-> authorized realization hook
-> verification hook
-> consumer-state hook
-> induced-consequence reharvest
-> exact-CID reversible duplicate subsumption
-> recursive closure
-> typed closure certificate.

Protected terminal distinctions:
CLOSED
OPEN
BLOCKED
PENDING_AUTHORIZATION represented as OPEN + resume condition.

Consumer states:
CONSUMED
CERTIFIED_NO_EFFECT
OPEN
BLOCKED
UNKNOWN.

UNKNOWN cannot falsely close.

Global harvest completeness remains OPEN and is not manufactured by the runtime.

### HF recursive host repair

Updated:
runtime/recursive_episode.py

Prior behavior:
terminal OPEN/BLOCKED closure returned before update_fn, which could discard typed terminal closure state.

Repair:
ClosureResult has admit_on_terminal=False by default.

When a TRC closure explicitly sets admit_on_terminal=True, typed OPEN/BLOCKED closure state is admitted before the episode returns.

Old fail-closed behavior remains the default.

### Big Equation facade

New:
runtime/inquiry_session.py

It directly realizes:

PEC
-> observer preparation when selected
-> observer reconcile
-> observer closure
-> HF recursive session
with closure interleaved before every state update/reentry.

The facade reuses recursive_episode.py.
It does not create a second HF controller.

## Regression evidence

New tests:
- tests/test_tool_run_closure.py
- tests/test_inquiry_session.py
- added terminal OPEN admission fixture to tests/test_recursive_episode.py

Protected cases tested:

1. induced consequences recursively enter TRC and settle;
2. exact duplicate administrative consequences are reversibly subsumed;
3. pending authorization is ACCOUNTED but remains OPEN;
4. unknown consumer state blocks false closure;
5. typed terminal OPEN state can be admitted through the recursive episode;
6. original prompt:
   "Run the equation on itself, then run Goal and then run Architect."
   automatically takes observer-first entry;
7. observer result crosses TRC before the core HF session;
8. core round sees the closed observer consequence;
9. observer OPEN stops before goal-directed core execution while preserving OPEN state.

GitHub Actions:
Take-5 Validation run 139
job validate = SUCCESS.

## Current runtime truth

IMPLEMENTED_AND_TESTED:
- entry contract binding;
- ICC controller latch;
- observer-risk selection;
- observer-first ordering;
- observer closure handoff;
- generic TRC orchestration;
- induced consequence recursion;
- typed OPEN/BLOCKED/PENDING closure;
- HF recursive interleaving;
- terminal OPEN/BLOCKED state admission when licensed;
- executable Big Equation facade;
- original self-application regression.

STILL OPEN:
- global/domain-independent harvest completeness;
- full domain-specific binding of every TRC realization/verification/consumer hook;
- exact global continuation equivalence;
- fairness/minimal continuation basis proofs;
- runtime promotion of IC-028;
- host-level persistence between user turns.

## Authority boundary

This is runtime realization evidence inside Take-5 successor development.

It does not promote IC-028 over IC-018.
It does not claim every domain handler is bound.
It does not claim global closure.

## Verdict

The prior broad statement:

"full native runtime equivalence to canonical TRC/HF001 remains OPEN"

is now too coarse.

Replace with:

GENERIC_TRC_ORCHESTRATION_RUNTIME = IMPLEMENTED_AND_TESTED.
HF_RECURSIVE_INTERLEAVING_RUNTIME = IMPLEMENTED_AND_TESTED.
BIG_EQUATION_FACADE = IMPLEMENTED_AND_TESTED.
DOMAIN_HARVEST_AND_EFFECT_BINDINGS = BASIS_RELATIVE / PARTIAL / OPEN.
RUNTIME_PROMOTION = NOT AUTHORIZED.
