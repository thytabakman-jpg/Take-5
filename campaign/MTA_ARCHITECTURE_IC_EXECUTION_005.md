# MTA + Architecture Reanalysis + IC Execution 005

Date 2026-09-24
Status EXECUTED
Authority nonproduction only

## MTA on migration-readiness plan

Input plan was six sequential phases: capability reconstruction, historical regression, architecture attack, hard cases, closure attack, readiness packet.

Material delta 1
The phases are not strictly sequential. Reconstruction, regression and architecture attack must form a coupled loop because implementing a capability can expose a missing architectural factor.

Use:
X*=Fix(Reconstruct,Regress,Attack,Repair)(A,H,E)

where A architecture, H protected behavior universe, E execution evidence.

Material delta 2
"Implement 58 capabilities" is too coarse. The protected set has at least three levels:
atomic/provisional behaviors H,
composite programs P,
historical execution claims E_hist.
Passing H alone does not prove P or E_hist.

Material delta 3
Readiness needs two independent coordinates:
semantic sufficiency and realization sufficiency.

ReadyRelative iff
Reconstructs(H) AND Regresses(E_hist) AND HoldoutPass AND NoBypass AND RuntimeBound AND ClosureRelative AND OpensTypedNonblocking.

Material delta 4
Testing must consume failures as architecture evidence:
failure -> Diagnose -> MTA/Architecture -> repair architecture/program/runtime -> rerun affected closure.
A failing test is not merely code repair.

MTA disposition
Replace phase waterfall with evidence-driven fixed-point campaign.

## Architecture Analysis on the plan

Plan object:
Campaign=<Goal,ProtectedSet,WorkGraph,EvidenceGraph,Authority,State,Transitions,Closure>

Required work graph:
W1 exact behavior registry
W2 executable program binding
W3 atomic reconstruction fixtures
W4 composite reconstruction fixtures
W5 historical matched regressions
W6 authority/bypass/concurrency/self-modification fixtures
W7 zero-request and unfamiliar holdouts
W8 role/operator ablation
W9 relative closure/corpus rescan
W10 readiness packet

Edges are dependency-sensitive, not a simple chain.
W1->W2->W3.
W3 can update architecture and reenter W1/W2.
W4/W5 depend on W2/W3 but can expose new H.
W6 begins immediately and continues.
W7 only after enough implementation exists to avoid trivial failure.
W8 after representative reconstruction exists.
W9 after W1-W8 reach local stability.
W10 only after W9.

Plan architecture PASS after replacing waterfall with this graph.

## Architecture Analysis on A5

A5 semantic basis:
T=<K,S,O,G,M,C,R,U>

Strengths:
1 behavior-first rather than named-tool-first;
2 generation, admission and transition separated;
3 authoritative effect law explicit;
4 state/provenance/authority represented;
5 modifiers cover representation/arity/order/interaction;
6 routing and reentry explicit;
7 concrete tools are programs, allowing unbounded ecology without kernel growth.

Material weaknesses exposed:
A. Program contract is described but not yet first-class executable registry.
B. Witness schema exists but validation obligations are not enforced after transition.
C. State history is in-memory fixture, not durable/replayable.
D. C disposition product remains compressed in runtime.
E. no executable noncommutation protocol.
F. no capability-to-program reconstruction ledger.
G. no composite-program interface.
H. no explicit external observation/action boundary in runtime.
I. no self-modification special fixture.
J. exact O four-factor minimality remains untested.

Architecture disposition:
A5 is strong enough to test but not strong enough to validate.
Do not redesign semantic roles now.
Strengthen realization surfaces around the eight-role basis and let tests force semantic changes.

## Improvement Core selected campaign

Highest leverage next move is not more prose architecture.
Build the executable program/capability registry and make coverage mechanically testable.

Reason:
It connects the exact C01-C49 and CAP-001..033 evidence to runtime A5 and turns "recovered" into falsifiable reconstruction claims.

Immediate sequence:
1 create typed ProgramSpec/registry;
2 enroll all C01-C49 and CAP-001..033 with behavior-family bindings and validation state;
3 reject duplicate ID / missing role / unbound protected-output records;
4 run registry integrity tests;
5 then replace declarative bindings with executable adapters family by family;
6 failures reenter MTA + Architecture automatically in campaign ledger.

## Governing completion rule

Do not claim move-in readiness until:
forall h in H_protected, ReconstructionWitness(h)
and all required historical/composite/holdout/governance gates pass
and closure attack returns no blocking residual.

Migration remains user-authorized only.
