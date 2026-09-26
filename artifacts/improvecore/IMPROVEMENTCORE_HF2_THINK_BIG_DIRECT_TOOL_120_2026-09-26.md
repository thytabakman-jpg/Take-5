# ImprovementCore + HF2 Think-Big Pass 120

Date: 2026-09-26
Command: Think big.
Controller: ImprovementCore / IC-028
HF2: explicit validated campaign composition
Input successor: Stage-1 direct-tool/HF2 runtime repair
Stage-1 validation:
- Take-5 Validation 36270157882 SUCCESS
- Capability Preservation 36270157829 SUCCESS

## Whole-system observation

Stage 1 closed the runtime seam:

- direct imperative commands can resolve to the registered tool;
- the current full configured plan is bound;
- the ImprovementCore selected-tool bridge and direct-command gateway share one HF2 execution primitive;
- HF2 actually reapplies a live/material capability;
- missing adapters remain OPEN.

The remaining repository-owned weakness is identity-level.

ConfiguredRunSpec still does not state which recurrence engine belongs to a configured invocation.

ToolExecutionPlan still does not carry recurrence as a protected coordinate.

Tool manifests still do not reconstruct recurrence as a generic protected behavior.

Therefore the runtime repair can regress if a future caller builds a full plan and invokes a native adapter without using the shared recurrence primitive.

## Think-big candidate frontier

A. LEAVE_HF2_AS_RUNTIME_CONVENTION

Reject:
the original failure class can recur through a new parallel executor.

B. ADD_HF2_TO_DOCUMENTATION_ONLY

Reject:
no machine-checkable invariant.

C. PROMOTE_RECURRENCE_INTO_CONFIGURED_IDENTITY

Effect:
ConfiguredRunSpec, ToolExecutionPlan, manifests, direct gateway, selected-tool bridge, and portfolio audit all agree on one recurrence coordinate.

For ordinary registered tools:

RecurrenceEngine(T)=HF002.

For HF002:

RecurrenceEngine(HF002)=SELF.

D. WRAP_HF002_INSIDE_HF002

Reject:
category error and unnecessary recursion.

E. UNIVERSAL_CHATGPT_HOST_INTERCEPTION

Disposition:
EXTERNAL_NOT_OWNED.

## ImprovementCore selection

Selected:

PROMOTE_RECURRENCE_INTO_CONFIGURED_IDENTITY.

## Required implementation

1. ConfiguredRunSpec gains:
   recurrence_required,
   recurrence_engine,
   invocation_profile.

2. ConfiguredRunSpec.complete() fails unless recurrence is:
   HF002 for ordinary registered tools,
   SELF for HF002.

3. ToolExecutionPlan carries the recurrence identity and treats it as part of plan completeness.

4. Generic tool manifests reconstruct:
   CONFIGURED_HF2_RECURRENCE,
   FULL_CONFIGURED_INVOCATION_PROFILE.

5. The shared HF2 executor reads recurrence from the plan instead of inferring it from the tool name.

6. The selected-tool bridge reports recurrence from the configured plan.

7. A whole-portfolio audit proves every current registered tool:
   - has a complete full invocation profile;
   - resolves through a direct command;
   - binds 36 cells / 792 questions / 144 cognitive projections;
   - reaches the shared recurrence executor;
   - produces an HF2 or SELF recurrence receipt;
   - fails closed when the adapter is absent.

## HF2 recurrence of this ImprovementCore pass

Round 0:
runtime success versus identity protection separated.
Material delta:
recurrence becomes a load-bearing configured identity coordinate.
HF2 -> REAPPLY_C.

Round 1:
manifest reconstruction and portfolio enforcement added.
Material delta:
future alternate callers now fail configured identity/plan audits when recurrence is missing.
HF2 -> REAPPLY_C.

Round 2:
whole-portfolio audit verifies current repertoire.
No remaining repository-owned recurrence seam changes the selected repair.
HF2 -> RELATIVE_CLOSE.

## Boundary

Repository-owned full invocation:
target CLOSED_RELATIVE.

Universal external host interception:
EXTERNAL_NOT_OWNED.

The repository can make every Take-5-governed formal-tool command fail closed unless the full invocation profile is present. It cannot force an unrelated host that never enters Take-5.
