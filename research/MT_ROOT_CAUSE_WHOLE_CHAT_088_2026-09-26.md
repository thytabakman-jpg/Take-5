# MT on "Rout Cause" and Current Chat 088

Date: 2026-09-26
Status: SEMANTIC MT RECONSTRUCTION / BUILD INPUT

## Frozen job

Recover what the user meant by the Root Cause tool from:
- the phrase "Rout Cause";
- the current conversation;
- recovered historical Root Cause artifacts;
- current ImproveCore/HF1/HF2 architecture.

Then derive the tool behavior before implementation.

## MT on the phrase

Transforms tested:

1. spelling:
Rout Cause -> Root Cause

Result:
nonmaterial.

2. punctuation:
Root Cause -> root-cause

Result:
nonmaterial.

3. semantic weakening:
root cause -> a cause

Result:
material.

4. selector weakening:
smallest stable upstream generator
-> earliest observed cause

Result:
material.

5. recurrence removal:
recurring failure class
-> single observed incident

Result:
material.

6. representation-stability removal:
candidate must survive representation changes
-> candidate only has to fit the current representation

Result:
material.

7. counterfactual removal test removed

Result:
material.

Conclusion:
the protected semantic nucleus is not the phrase spelling.
It is the rootness selector.

## MT on the current chat

Repeated transformations expose stable failure classes:

A.
"the capability exists"
versus
"the capability is on the mandatory operating path".

Material.

B.
"documented current"
versus
"runtime current".

Material.

C.
"configured full run"
versus
"named/bare invocation".

Material.

D.
"repository invariant"
versus
"user-visible response boundary".

Material.

E.
"migration copied artifacts"
versus
"migration reconstructed protected behavior and activation".

Material.

F.
"local tool result"
versus
"parent controller/global completion".

Material.

## Recovered desired RootCause behavior

The user's desired tool repeatedly asks a deeper question after an apparent cause:

"What generated this failure class, and what generated that?"

It should not ritualistically recurse forever.

It recurs only when the changed causal representation exposes a material local
discrimination frontier.

Desired behavior:

Freeze recurring failure class
-> recover current causal representation
-> generate/accept rival mechanisms
-> distinguish symptom/mechanism/enabling/configuration/representation/root-generator roles
-> challenge each candidate for recurrence coverage
-> challenge representation stability
-> challenge with counterevidence
-> run counterfactual removal test
-> preserve nondominated rivals
-> reapply RootCause through HF2 when the causal state materially changes
-> local close only after smaller-generator challenge
-> return local result to ImproveCore
-> ImproveCore admits/replans globally.

## Main whole-chat result candidate

Narrow causes repeatedly found in this chat include:
- finite alias list;
- stale recovery document;
- missing dispatcher;
- generic-only tool manifest;
- recursive component present but inactive.

These are real mechanisms but do not explain the whole recurrence class.

The stronger generator is:

PROTECTED_TRANSITION_INTEGRITY_FAILURE

Meaning:
a protected behavior is represented somewhere in the system but there is no single
mandatory, reconstructible, verified chain ensuring it survives:

canonical identity
-> configured dispatch
-> execution
-> result consumption
-> state update
-> reentry
-> final user-visible boundary.

This generator explains why different local fixes repeatedly worked and then failed at
another transition boundary.

## Architecture consequence

The strongest RootCause successor should be:
- a configured formal tool;
- HF2-wrapped for local same-capability recurrence;
- HF1-aware for upstream invalidation;
- TRC-gated;
- ImprovementCore-managed at the parent level;
- fail-open on missing rootness evidence;
- explicit about local versus global closure.

This MT result is the build basis for RootCause Mathematics 087.
