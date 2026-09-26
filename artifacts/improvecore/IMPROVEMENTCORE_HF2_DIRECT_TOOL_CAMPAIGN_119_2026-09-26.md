# ImprovementCore + HF2 Direct-Tool Campaign 119

Date: 2026-09-26
Controller: ImprovementCore / IC-028
HF2: explicit validated campaign composition
Inputs:
- MT_DIRECT_TOOL_HF2_PROMPT_118
- GOAL_DIRECT_TOOL_HF2_PROMPT_118
- IC123_REWRITE_DIRECT_TOOL_HF2_118

## Evidence-only entry

The upstream MT/GOAL/IC123 artifacts are evidence. They do not self-authorize a patch.

ImprovementCore reconstructs the candidate frontier.

## Candidate frontier

A. DOCUMENT_HF2_AS_REQUIRED

Effect:
wording only.

Reject:
does not cause recurrence.

B. WRAP_ONLY_DIRECT_COMMANDS

Effect:
direct commands receive HF2.

Residual:
ImprovementCore selected-tool bridge remains a weaker one-shot parallel path.

C. WRAP_ONLY_IMPROVEMENTCORE_BRIDGE

Effect:
controller-selected tools receive HF2.

Residual:
free-standing direct commands still lack a canonical gateway.

D. SHARED_CONFIGURED_HF2_EXECUTION_PRIMITIVE

Effect:
one execution primitive composes a bound configured plan with HF002 and is reused by:
- ImprovementCore selected-tool bridge;
- direct-command gateway.

Preserves:
ConfiguredRunSpec,
global D36 plan,
PTI,
tool manifests,
tool-native adapters.

E. UNIVERSAL_HOST_INTERCEPTION

Disposition:
EXTERNAL_NOT_OWNED.

## ImprovementCore selection

Selected:

SHARED_CONFIGURED_HF2_EXECUTION_PRIMITIVE.

Reason:

It removes both repository-owned parallel-path defects with one reusable primitive and does not
duplicate the current wrapper/PTI stack.

## HF2 recurrence for ImprovementCore itself

Round 0:
recover plan-versus-invocation distinction.

Material delta:
HF2 availability is separated from HF2 attachment.

HF2:
REAPPLY_C.

Round 1:
recover bridge-versus-direct-command parallel-path distinction.

Material delta:
shared execution primitive dominates two local patches.

HF2:
REAPPLY_C.

Round 2:
select shared primitive and direct command gateway.

No further local distinction changes the selected repository-owned repair.

HF2:
RELATIVE_CLOSE.

## Stage-1 implementation target

1. runtime/configured_hf2_execution.py
2. modify runtime/improvement_core_tool_bridge.py to call it
3. runtime/direct_tool_command_gateway.py
4. direct-command and bridge recurrence regressions

## Deliberately deferred to final Think-big pass

Whether HF2 recurrence must become a protected coordinate of ConfiguredRunSpec/tool manifests
is left for the final whole-system ImprovementCore pass.

That decision is not pre-authorized here.
