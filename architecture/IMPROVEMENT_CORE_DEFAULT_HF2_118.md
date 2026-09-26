# ImprovementCore Default HF2 Recurrence 118

Date: 2026-09-26
Status: CURRENT / VALIDATED / MERGED
Controller: ImprovementCore / IC-028
Candidate regime: 091

## Problem

Repeated successful use of explicit HF2[ImprovementCore] campaigns showed a manual-reprompt seam.

The user had to ask for:

ImprovementCore with HF2

to obtain same-capability recurrence after a material completed pass.

Validated evidence already existed in:
- ImprovementCore + HF2 observer campaign 115;
- Think-Big selection 116;
- Think-Big fix closure 117.

Those runs showed that HF2 can reapply the same ImprovementCore capability after material local
change and stop at relative closure without taking over global tool selection.

## Promotion

User-facing ImprovementCore now resolves to:

ImprovementCore_091
=
HF2[
  ImprovementCore_one_pass
].

The direct low-level function

run_improvement_core_regime(...)

remains the one-pass surface for debugging, experiments and explicit controlled composition.

The normal user-facing dispatch uses:

run_improvement_core_with_hf2(...).

## Recurrence predicate

Let IC(x) be one complete current ImprovementCore regime pass.

Let M_t mean that the pass emitted a material-effect witness.

Let DeltaSem_t mean that the normalized semantic state changed:

DeltaSem_t
iff
Fingerprint(x_(t+1))
!=
Fingerprint(x_t).

Then local reapplication is licensed only when:

M_t
and
DeltaSem_t
and
LocalHF2Enabled_t
and
HF1_t = STABLE.

Thus a handler that repeatedly reports "material" without changing the semantic state cannot
force recurrence forever.

## Closure

Relative local closure is reached when:

IC_status = COMPLETE

and

not (M_t and DeltaSem_t).

HF1 dispositions REENTER / OPEN / BLOCKED / CONFLICT escape the local loop immediately.

RESOURCE_STOP is OPEN, not completion.

## Role separation

HF2 owns:
same-capability local recurrence.

ImprovementCore owns:
global work discovery;
candidate selection;
cross-capability routing;
admission;
knowledge integration;
longitudinal progress;
global reentry and terminality.

HF1 owns:
upstream invalidation and reentry classification.

TRC owns:
consequence closure.

Therefore:

HF2[ImprovementCore]
!=
HF2 as global controller.

## Identity promotion

Regime 091 adds an explicit ImprovementCore protected-behavior manifest.

Required protected clusters include:
- controller ownership;
- observer-first mode;
- configured-tool execution;
- recursive parent control;
- default HF2 local recurrence;
- durable negative learning;
- durable material knowledge capture;
- strict progress;
- external acquisition;
- plural-frontier preservation;
- generic protected-transition integrity.

This closes the previous generic-only manifest gap for ImprovementCore if validation passes.

## Boundary

This does not promote HF2 as a universal wrapper over every Take-5 tool.

It promotes HF2 only as the default local recurrence operator of user-facing ImprovementCore.

## Validation target

The promotion is admitted only if:
1. a material first pass re-enters;
2. an unchanged second pass reaches RELATIVE_CLOSE;
3. state change without material witness does not re-enter;
4. HF1 upstream REENTER escapes local HF2;
5. hf2_enabled=False preserves the one-pass debugging path;
6. direct run_improvement_core_regime remains one-pass;
7. ImprovementCore becomes explicit rather than generic-only in manifest audit;
8. the full Take-5 suite passes;
9. Capability Preservation passes.


## Promotion evidence

PR #116
- merge: ef2ef2a6fa0c4093c28654f4fda04d68eb4d9869
- Take-5 Validation: 36270165005 SUCCESS
- Capability Preservation: 36270165051 SUCCESS

Regime 091 is now the current user-facing ImprovementCore regime.
