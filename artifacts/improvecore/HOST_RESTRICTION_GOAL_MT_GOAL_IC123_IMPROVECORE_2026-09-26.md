# Host Restriction / Tool Downgrade Audit

Date: 2026-09-26
Repository basis: main @ f35577993d076e9113db0bc6e62b91d89b062565
Requested sequence: GOAL -> MT -> GOAL -> IC123 -> ImprovementCore
Status: CLOSED_RELATIVE / EXTERNAL_HOST_RESIDUAL

## User problem

Determine whether the recurring problem of ChatGPT restricting, weakening, compressing, or partially executing formal Take-5 tools has been fully solved, and seek a system-wide solution for every tool invocation.

The governing distinction is between:

1. repository-owned invocation weakening, which Take-5 can govern; and
2. external host rules or host non-interception, which Take-5 cannot compel from inside the repository.

The target is not removal of mandatory host/platform policy. The target is elimination of silent tool degradation.

## GOAL pass 1

For every registered formal tool T and every Take-5-governed invocation request:

the system must either

FULL_EXECUTE(T)

with the current configured identity, wrapper, D36_C, native layers, question/cognitive projections, closure/reentry, PTI, and configured recurrence,

or

FAIL_CLOSED(T, typed blocker).

A prose substitute, compressed core, planning-only answer, partial wrapper, one-shot adapter call, or tool label does not count as execution.

Universal success over arbitrary external ChatGPT sessions requires an additional host-side premise:

HOST_INTERCEPTS_AND_INVOCES_TAKE5.

That premise is not supplied by repository code alone.

## MT pass

### Recovered facts

Current full invocation profile:
FULL_CONFIGURED_HF2_V1.

For ordinary registered tools:
Rec(T)=HF002.

For HF002:
Rec(HF002)=SELF.

Current repository-owned full invocation routes include:

1. direct imperative formal-tool commands;
2. ImprovementCore selected-tool execution;
3. PTI end-to-end configured transitions;
4. ToolConductor factor execution.

PR #119 merged at:
f35577993d076e9113db0bc6e62b91d89b062565

and explicitly closed additional PTI and ToolConductor weaker paths after the prior full-invocation repair.

### Material distinctions

D1. FULL_TOOL_IDENTITY != HOST_INTERCEPTION

Take-5 can make the invoked tool complete once the request enters Take-5. It cannot force an unrelated host session to enter Take-5.

D2. HOST_POLICY != TOOL_DOWNGRADE

Mandatory platform/system/safety rules are external authority constraints. They are not a repository defect and cannot be removed by a Take-5 wrapper.

Accidental weakening, compression, substitution, or partial execution is a tool-integrity defect and is governed fail-closed inside Take-5.

D3. CORRECT_REPOSITORY != UNIVERSAL_CHAT_BEHAVIOR

A repository proof does not establish that every future ChatGPT response loads or calls the repository.

D4. EXECUTION_CLAIM != EXECUTION_RECEIPT

A user-visible claim that a formal tool ran is valid only when an execution path supplies the governed configured-run receipt. Otherwise the truthful disposition is OPEN/BLOCKED/EXTERNAL_NOT_BOUND.

D5. MORE_INTERNAL_WRAPPERS != HOST_CONTROL

Adding another wrapper inside Take-5 does not change the prefix of an external host episode that never invokes Take-5.

### MT result

Repository-owned silent downgrade:
CLOSED_RELATIVE.

Universal external ChatGPT interception:
EXTERNAL_NOT_OWNED.

Mandatory host/platform restrictions:
EXTERNAL_AUTHORITY_CONSTRAINT.

## GOAL pass 2

Define the system-wide non-silent-degradation contract:

For every formal-tool request T:

VALID_TOOL_RESPONSE(T)
iff
VERIFIED_FULL_EXECUTION_RECEIPT(T)
or
EXPLICIT_TYPED_BLOCKER(T).

Never certify RUN(T) from naming, memory, familiarity, generic reasoning, or partial reconstruction.

A future external host integration reaches the desired universal behavior only when the host itself guarantees:

formal-tool command
-> Take-5 canonical dispatcher
-> FULL_CONFIGURED_HF2_V1
-> native adapter
-> recurrence
-> closure/reentry
-> execution receipt
-> user-visible emission.

Until that host hook exists, universal interception cannot be truthfully marked closed.

## IC123 residual separation and handoff

IC123 preserves these residuals:

R1. Direct-command, selected-tool, PTI, and ToolConductor repository paths are already governed by the full configured invocation profile.

R2. The remaining recurring class is not another internal wrapper gap.

R3. The external host can still bypass Take-5 by never entering its dispatcher.

R4. Mandatory external host/platform rules cannot be neutralized by repository code.

R5. The correct fail-closed user-visible law is:
no full execution receipt -> no claim that the formal tool ran.

### IC123 handoff to ImprovementCore

ImprovementCore, treat the repository-owned full-invocation repair and PR #119 as evidence.

Do not reopen already-closed internal paths without contradictory evidence.

Determine whether any owned execution path still allows a formal Take-5 tool to be reported as run without the FULL_CONFIGURED_HF2_V1 receipt.

If none remains, preserve repository closure.

Then isolate the external host integration requirement. Do not misclassify host/platform authority as a repository bug and do not claim universal ChatGPT interception without an actual host-side hook.

The desired end-state is:

Take-5-owned route:
silent degradation impossible.

External host:
either invoke Take-5 and return a verified receipt, or expose an explicit EXTERNAL_NOT_BOUND / policy blocker rather than simulating the tool.

## ImprovementCore result

### Observation

Current main includes the post-merge Think-big repair in PR #119.

The current architecture explicitly proves that repository ownership does not entail universal host interception.

The current full invocation architecture routes all identified repository-owned full-tool surfaces through the shared configured HF2 execution profile.

### Selection

Preserve:
REPOSITORY_OWNED_FULL_INVOCATION = CLOSED_RELATIVE.

Preserve:
UNIVERSAL_HOST_INTERCEPTION = EXTERNAL_NOT_OWNED.

Adopt as the cross-boundary truth contract:

NO_EXECUTION_RECEIPT_NO_RUN_CLAIM.

### Answer to the user's question

No, the entire problem is not fully solved at the universal ChatGPT-host level.

Yes, the Take-5-owned silent-downgrade problem is closed relative to the current identified repository execution surfaces.

The remaining universal problem cannot be solved by adding restrictions, wrappers, or recurrence inside Take-5. It requires a host-side integration that actually invokes Take-5 before claiming a formal tool ran.

Mandatory host/platform restrictions remain external authority constraints and are not removable by ImprovementCore.

## Reentry condition

Reopen this result when any of the following appears:

1. a repository-owned execution path bypasses FULL_CONFIGURED_HF2_V1;
2. a user-visible run claim lacks an execution receipt;
3. a new host integration hook becomes available;
4. a current host integration bypasses or weakens the canonical dispatcher;
5. PR #119 or its protected behaviors regress.

