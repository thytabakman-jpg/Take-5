# ImproveCore Two-Episode Tool Run Input 105

Date: 2026-09-26
Status: USER-DIRECTED EXECUTION INPUT

## User request

Run ImproveCore and tell it to run MT and Architect and Root Cause. Then run a different ImproveCore.

## Interpretation

Episode A:
- current ImproveCore owns orchestration;
- execute the current configured full-wrapper D36_C contracts for MT, Architecture/Architect, and RootCause;
- use actual semantic runtime where present;
- where the repository exposes only partial semantic runtime, execute the available current governed surface and preserve execution truth as SEMANTICALLY_APPLIED or OPEN rather than upgrading it to IMPLEMENTATION_EXECUTED;
- inspect any invocation/runtime mismatch discovered by those tools.

Episode B:
- start a fresh, independent ImproveCore state after Episode A;
- consume Episode A results as evidence;
- challenge its conclusions;
- identify a strict-gain repair when one is justified;
- do not inherit Episode A terminality or state by reference.

## Protected constraints

- ordinary tool run means configured, wrapper-required, recursive, closure/reentry required, D36_C;
- do not substitute a bare/core tool;
- preserve OPEN/BLOCKED/CONFLICT;
- do not claim standalone native runtime execution where only a semantic host binding exists;
- do not treat registry presence as proof of user-invocation reachability.
